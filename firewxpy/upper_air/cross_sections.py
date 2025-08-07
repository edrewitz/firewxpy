
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import metpy.plots as mpplots
import metpy.calc as mpcalc
import numpy as np
import firewxpy.parsers as parsers
import firewxpy.geometry as geometry
import firewxpy.colormaps as colormaps
import pandas as pd
import matplotlib.gridspec as gridspec
import firewxpy.settings as settings
import firewxpy.standard as standard
import firewxpy.dims as dims
import os
import time as tim
import matplotlib.dates as md
import xarray as xr

from matplotlib.patheffects import withStroke
from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from dateutil import tz
from firewxpy.calc import scaling, Thermodynamics, unit_conversion
from firewxpy.utilities import file_functions
from metpy.units import units
from firewxpy.data_access import model_data, station_coords
from metpy.interpolate import cross_section

mpl.rcParams['xtick.labelsize'] = 6
mpl.rcParams['ytick.labelsize'] = 6
mpl.rcParams['font.weight'] = 'bold'
local_time, utc_time = standard.plot_creation_time()

datacrs = ccrs.PlateCarree()

provinces = cfeature.NaturalEarthFeature(category='cultural', 
    name='admin_1_states_provinces_lines', scale='50m', facecolor='none', edgecolor='k')

props = dict(boxstyle='round', facecolor='wheat', alpha=1)

class time_cross_sections:

    r'''
    This class hosts time vs. height cross-sections of a specific parameter for a specific point. 
    Motivated by Dr. Brian Tang's WxChallenge Model Guidance page: https://www.atmos.albany.edu/facstaff/tang/forecast/

    '''

    def plot_lower_atmosphere_wind(model, station_id, save_name, longitude=None, latitude=None, data=False, ds=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-'):
    
        r'''
            This function plots a time vs. pressure cross-section forecast for a given point. Paramter: Lower Atmosphere Wind. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) NAM - North American Model
                   3) RAP - RAP for the CONUS
                   4) RAP 32 - 32km North American RAP
    
            2) station_id (String) - The 4-letter airport station identifier. 
                                     If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

            3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                                    Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 
    
            Optional Arguments:
    
            1) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 
            
            2) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 
            
            3) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                and passing the data in or if the function needs to download the data. A value of False means the data
                is downloaded inside of the function while a value of True means the user is downloading the data outside
                of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                things, it is recommended to set this value to True and download the data outside of the function and pass
                it in so that the amount of data requests on the host servers can be minimized. 
    
    
            4) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 
    
            5) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                     wishes to use a reference system not on this list, please see items 17-23. 
                
                Reference Systems: 
                
                1) 'States & Counties'
                2) 'States Only'
                3) 'GACC Only'
                4) 'GACC & PSA'
                5) 'CWA Only'
                6) 'NWS CWAs & NWS Public Zones'
                7) 'NWS CWAs & NWS Fire Weather Zones'
                8) 'NWS CWAs & Counties'
                9) 'GACC & PSA & NWS Fire Weather Zones'
                10) 'GACC & PSA & NWS Public Zones'
                11) 'GACC & PSA & NWS CWA'
                12) 'GACC & PSA & Counties'
                13) 'GACC & Counties'
    
    
            6) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide state borders. 
    
            7) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide county borders. 
    
            8) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display GACC borders. 
    
            9) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display PSA borders.
    
            10) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display CWA borders.
    
            11) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.
    
            12) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.
    
            13) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 
    
            14) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 
    
            15) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 
    
            16) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 
    
            17) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 
    
            18) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 
    
            19) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 
    
            20) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 
    
            21) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                To change to a dashed line, users should set state_border_linestyle='--'. 
    
            22) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                To change to a dashed line, users should set county_border_linestyle='--'. 
    
            23) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                To change to a dashed line, users should set gacc_border_linestyle='--'. 
    
            24) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            25) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            26) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            27) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'.   
    
            Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}
        
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones
    
            state_border_linewidth = state_border_linewidth
            county_border_linewidth = county_border_linewidth
            gacc_border_linewidth = gacc_border_linewidth
            cwa_border_linewidth = cwa_border_linewidth
            nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
            nws_public_zones_linewidth = nws_public_zones_linewidth
            psa_border_linewidth = psa_border_linewidth
    
        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
                state_border_linewidth=1 
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                state_border_linewidth=1 
                county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
                gacc_border_linewidth=1
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
                cwa_border_linewidth=1
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                cwa_border_linewidth=1
                nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                cwa_border_linewidth=1
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                cwa_border_linewidth=1
                county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_public_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                cwa_border_linewidth=0.25
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                county_border_linewidth=0.25 
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                county_border_linewidth=0.25 

        if data == False:
            if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
                ds = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
                
                longitude = ds['tmpprs']['lon'].values
                latitude = ds['tmpprs']['lat'].values
        
            else:
                if model == 'RAP 32' or model == 'rap 32':
                    ds = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
                else:
                    ds = model_data.get_nomads_opendap_data_point_forecast(model, station_id, longitude, latitude)
                
                
        if data == True:
    
            ds = ds.squeeze()
    
            if station_id == 'Custom' or station_id == 'custom':
                longitude = longitude 
                latitude = latitude
                
            else:
                longitude, latitude = station_coords(station_id)
    
            if model == 'GFS0p25' or model == 'GFS0p50' or model == 'NA NAM' or model == 'RAP 32' or model == 'rap 32':
                
                if longitude < 0:
                    longitude = 360 + longitude
                else:
                    longitude = longitude   
            
            ds = ds.sel(lon=longitude, lat=latitude, method='nearest')
        ds = ds.sel(time=ds['time'][0:29])
        if model == 'NAM' or model == 'RAP' or model == 'RAP 32':
            ds = ds.sel(lev=ds['lev'][0:21])
        if model == 'GFS0p25':
            ds = ds.sel(lev=ds['lev'][0:13])
    
        if station_id == 'Custom' or station_id == 'custom':
            longitude = longitude
            latitude = latitude
    
        else:
            longitude = ds['tmpprs']['lon'].values
            latitude = ds['tmpprs']['lat'].values
    
        if longitude > 180:
            longitude = (360 - longitude) * -1
        else:
            longitude = longitude
    
    
        path, path_print = file_functions.forecast_cross_sections_graphics_paths(model, 'Time Cross Section', 'Lower Atmosphere Winds', reference_system)
    
        try:
            os.remove(f"{path}/{save_name}")
        except Exception as e:
            pass
    
        print(f"The old {save_name} file in {path_print} has been deleted.")
    
        title_lon = str(round(float(abs(longitude)), 1))
        title_lat = str(round(float(abs(latitude)), 1))
    
        cmap = colormaps.cross_section_wind_speed()
    
        u = (ds['ugrdprs']) * 2.23694
        v = (ds['vgrdprs']) * 2.23694
    
        ws = mpcalc.wind_speed(u * units('mph'), v * units('mph'))
        
        time = ds['time']
        times = time.to_pandas()
        sfc_pressure = (ds['pressfc'][:]) / 100
        pressure = ds['ugrdprs']['lev']
        height_ft = (ds['hgtprs'][:, :]) * 3.28084
        height_sfc = (ds['hgtsfc'][:])  * 3.28084
        height_agl = height_ft - height_sfc
        pressure_grid, time_grid = np.meshgrid(pressure, time)
        temperature = ds['tmpprs'].to_numpy().flatten()
        lat = abs(round(float(ds['lat'].values), 1))
        lon = abs(round(float(ds['lon'].values), 1))
    
        if lon > 180:
            lon = 360 - lon
        else:
            lon = lon
    
        if lat >= 0:
            lat_symbol = '°N'
        else:
            lat_symbol = '°S'
    
        if lon <= 180:
            lon_symbol = '°W'
        else:
            lon_symbol = '°E'
        
        
        fig = plt.figure(figsize=(18, 7))
        fig.set_facecolor('aliceblue')
        gs = gridspec.GridSpec(10, 10)
    
        ax1 = fig.add_subplot(gs[0:10, 0:10])
        
        ax1.set_yscale('symlog')
        ax1.set_yticks(np.arange(1000, 50, -100))
        ax1.set_yticklabels(np.arange(1000, 50, -100))
        ax1.set_ylim(np.nanmax(sfc_pressure), 475)
        ax1.xaxis.set_major_formatter(md.DateFormatter('%d/%HZ'))
        ax1.set_xticks(time)
    
        stop = np.nanmax(ws[:,:])
    
        end = stop + 1
        nearest_10 = (round((stop/10),0) * 10) + 10
        nearest_5 = (round((stop/5),0) * 5) + 10
                            
        ax1.contourf(time_grid, pressure_grid, ws[:, :], levels=np.arange(0, end, 1), cmap=cmap, alpha=0.25, extend='max')
        c10 = ax1.contour(time_grid, pressure_grid, ws[:, :], levels=np.arange(0, nearest_10, 10), colors='black', zorder=2, linewidths=1)
        ax1.clabel(c10, levels=np.arange(0, nearest_10, 10), inline=True, fontsize=8, rightside_up=True)
        c5 = ax1.contour(time_grid, pressure_grid, ws[:, :], levels=np.arange(5, nearest_5, 10), colors='black', zorder=2, linewidths=1, linestyles='--')
        ax1.clabel(c5, levels=np.arange(5, nearest_5, 10), inline=True, fontsize=8, rightside_up=True)
        ax1.barbs(time_grid, pressure_grid, u[:, :], v[:, :], clip_on=True, zorder=10, color='black', length=5, alpha=0.5)
        if station_id != 'Custom' or station_id != 'custom':
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: WIND SPEED [MPH]\nSTATION: {station_id.upper()} - LAT: {str(lat)}{lat_symbol} | LON: {str(lon)}{lon_symbol}", fontsize=10, fontweight='bold', loc='left')
        else:
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: WIND SPEED [MPH]\nLAT: {str(lat)}{lat_symbol} | LON: {str(lon)}{lon_symbol}", fontsize=10, fontweight='bold', loc='left')
        try:
            plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[28].strftime('%a %d/%HZ')}", fontsize=8, fontweight='bold', loc='right')
        except Exception as e:
            plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[21].strftime('%a %d/%HZ')}", fontsize=8, fontweight='bold', loc='right')
        ax1.text(0.01, -0.08, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax1.text(0.8, -0.08, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
    
        wb = longitude - 6
        eb = longitude + 6
        nb = latitude + 3
        sb = latitude - 3
    
        ax2 = fig.add_subplot(gs[0:2, 8:10], projection=ccrs.PlateCarree())
        ax2.axis("off")
        ax2.set_extent([wb, eb, sb, nb], ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax2.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass    
    
        ax2.plot(longitude, latitude, marker='*', markersize=8, color='maroon', zorder=15)
        ax2.text(0.01, 0.01, "Reference System: "+reference_system, transform=ax2.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
    
        fig.savefig(f"{path}/{save_name}", bbox_inches='tight')
        plt.close(fig)
        print(f"Saved image of cross-section to {path_print}/{save_name}.")


    def plot_lower_atmosphere_vertical_velocity(model, station_id, save_name, longitude=None, latitude=None, data=False, ds=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-'):
    
        r'''
            This function plots a time vs. pressure cross-section forecast for a given point. Paramter: Vertical Velocity. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) NAM - North American Model
                   3) RAP - RAP for the CONUS
                   4) RAP 32 - 32km North American RAP
    
            2) station_id (String) - The 4-letter airport station identifier. 
                                     If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

            3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                                    Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 
    
            Optional Arguments:
    
            1) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 
            
            2) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 
            
            3) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                and passing the data in or if the function needs to download the data. A value of False means the data
                is downloaded inside of the function while a value of True means the user is downloading the data outside
                of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                things, it is recommended to set this value to True and download the data outside of the function and pass
                it in so that the amount of data requests on the host servers can be minimized. 
    
    
            4) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 
    
            5) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                     wishes to use a reference system not on this list, please see items 17-23. 
                
                Reference Systems: 
                
                1) 'States & Counties'
                2) 'States Only'
                3) 'GACC Only'
                4) 'GACC & PSA'
                5) 'CWA Only'
                6) 'NWS CWAs & NWS Public Zones'
                7) 'NWS CWAs & NWS Fire Weather Zones'
                8) 'NWS CWAs & Counties'
                9) 'GACC & PSA & NWS Fire Weather Zones'
                10) 'GACC & PSA & NWS Public Zones'
                11) 'GACC & PSA & NWS CWA'
                12) 'GACC & PSA & Counties'
                13) 'GACC & Counties'
    
    
            6) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide state borders. 
    
            7) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide county borders. 
    
            8) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display GACC borders. 
    
            9) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display PSA borders.
    
            10) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display CWA borders.
    
            11) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.
    
            12) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.
    
            13) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 
    
            14) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 
    
            15) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 
    
            16) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 
    
            17) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 
    
            18) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 
    
            19) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 
    
            20) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 
    
            21) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                To change to a dashed line, users should set state_border_linestyle='--'. 
    
            22) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                To change to a dashed line, users should set county_border_linestyle='--'. 
    
            23) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                To change to a dashed line, users should set gacc_border_linestyle='--'. 
    
            24) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            25) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            26) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            27) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'.   
    
            Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones
    
            state_border_linewidth = state_border_linewidth
            county_border_linewidth = county_border_linewidth
            gacc_border_linewidth = gacc_border_linewidth
            cwa_border_linewidth = cwa_border_linewidth
            nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
            nws_public_zones_linewidth = nws_public_zones_linewidth
            psa_border_linewidth = psa_border_linewidth
    
        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
                state_border_linewidth=1 
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                state_border_linewidth=1 
                county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
                gacc_border_linewidth=1
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
                cwa_border_linewidth=1
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                cwa_border_linewidth=1
                nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                cwa_border_linewidth=1
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                cwa_border_linewidth=1
                county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_public_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                cwa_border_linewidth=0.25
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                county_border_linewidth=0.25 
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                county_border_linewidth=0.25 

        if data == False:
            if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
                ds = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
                
                longitude = ds['tmpprs']['lon'].values
                latitude = ds['tmpprs']['lat'].values
        
            else:
                if model == 'RAP 32' or model == 'rap 32':
                    ds = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
                else:
                    ds = model_data.get_nomads_opendap_data_point_forecast(model, station_id, longitude, latitude)
                
                
        if data == True:
    
            ds = ds.squeeze()
    
            if station_id == 'Custom' or station_id == 'custom':
                longitude = longitude 
                latitude = latitude
                
            else:
                longitude, latitude = station_coords(station_id)
    
            if model == 'GFS0p25' or model == 'GFS0p50' or model == 'NA NAM' or model == 'RAP 32' or model == 'rap 32':
                
                if longitude < 0:
                    longitude = 360 + longitude
                else:
                    longitude = longitude   
            
            ds = ds.sel(lon=longitude, lat=latitude, method='nearest')
        ds = ds.sel(time=ds['time'][0:29])

        if model == 'NAM' or model == 'RAP' or model == 'RAP 32':
            ds = ds.sel(lev=ds['lev'][0:21])
        if model == 'GFS0p25':
            ds = ds.sel(lev=ds['lev'][0:13])
    
        if station_id == 'Custom' or station_id == 'custom':
            longitude = longitude
            latitude = latitude
    
        else:
            longitude = ds['tmpprs']['lon'].values
            latitude = ds['tmpprs']['lat'].values
    
        if longitude > 180:
            longitude = (360 - longitude) * -1
        else:
            longitude = longitude
    
    
        path, path_print = file_functions.forecast_cross_sections_graphics_paths(model, 'Time Cross Section', 'Lower Atmosphere Vertical Velocity', reference_system)
    
        try:
            os.remove(f"{path}/{save_name}")
        except Exception as e:
            pass
    
        print(f"The old {save_name} file in {path_print} has been deleted.")
    
        title_lon = str(round(float(abs(longitude)), 1))
        title_lat = str(round(float(abs(latitude)), 1))
    
        cmap = colormaps.vertical_velocity_colormap()
    
        u = (ds['ugrdprs']) * 2.23694
        v = (ds['vgrdprs']) * 2.23694
        vv = ds['vvelprs']
        
        time = ds['time']
        times = time.to_pandas()
        sfc_pressure = (ds['pressfc'][:]) / 100
        pressure = ds['ugrdprs']['lev']
        height_ft = (ds['hgtprs'][:, :]) * 3.28084
        height_sfc = (ds['hgtsfc'][:])  * 3.28084
        height_agl = height_ft - height_sfc
        pressure_grid, time_grid = np.meshgrid(pressure, time)
        temperature = ds['tmpprs'].to_numpy().flatten()
        lat = abs(round(float(ds['lat'].values), 1))
        lon = abs(round(float(ds['lon'].values), 1))
    
        if lon > 180:
            lon = 360 - lon
        else:
            lon = lon
    
        if lat >= 0:
            lat_symbol = '°N'
        else:
            lat_symbol = '°S'
    
        if lon <= 180:
            lon_symbol = '°W'
        else:
            lon_symbol = '°E'
        
        
        fig = plt.figure(figsize=(18, 7))
        fig.set_facecolor('aliceblue')
        gs = gridspec.GridSpec(10, 10)
    
        ax1 = fig.add_subplot(gs[0:10, 0:10])
        
        ax1.set_yscale('symlog')
        ax1.set_yticks(np.arange(1000, 50, -100))
        ax1.set_yticklabels(np.arange(1000, 50, -100))
        ax1.set_ylim(np.nanmax(sfc_pressure), 475)
        ax1.xaxis.set_major_formatter(md.DateFormatter('%d/%HZ'))
        ax1.set_xticks(time)

        low = np.nanmin(vv[:, :])
        high = np.nanmax(vv[:, :])

        if low < 0 and high >= 0:
            vv_range = abs(low) + high
        if low < 0 and high < 0 :
            vv_range = low - high
        if low >= 0 and high >= 0:
            vv_range = high - low

        step = round(vv_range/10, 1)

        if low < 0 and abs(low) > high and high >=0:
            upper_bound = round(abs(low),2)
            lower_bound = round(low,2)
        if low < 0 and high >= 0 and abs(low) <= high:
            lower_bound = round((high * -1),2)
            upper_bound = round(high,2)
        if low < 0 and high < 0:
            upper_bound = round(high,2)
            lower_bound = round(low,2)
        if low >= 0 and high >= 0:
            upper_bound = round(high,2)
            lower_bound = round(low,2)
        
        step_cs = round(vv_range/100, 2)
                            
        ax1.contourf(time_grid, pressure_grid, vv[:, :], levels=np.arange(lower_bound, (upper_bound + step_cs), step_cs), cmap=cmap, alpha=0.25, extend='both')
        c = ax1.contour(time_grid, pressure_grid, vv[:, :], levels = np.arange(round(low, 1), round((high+step),1), round(step,1)), colors='black', zorder=2, linewidths=1, linestyles='--')
        ax1.clabel(c, levels = np.arange(round(low, 1), round((high+step),1), round(step,1)), inline=True, fontsize=8, rightside_up=True)
        if station_id != 'Custom' or station_id != 'custom':
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: VERTICAL VELOCITY [Pa/s]\nSTATION: {station_id.upper()} - LAT: {str(round(lat,1))}{lat_symbol} | LON: {str(round(lon,1))}{lon_symbol}", fontsize=10, fontweight='bold', loc='left')
        else:
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: VERTICAL VELOCITY [Pa/s]\nLAT: {str(round(lat,1))}{lat_symbol} | LON: {str(round(lon,1))}{lon_symbol}", fontsize=10, fontweight='bold', loc='left')
        try:
            plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[28].strftime('%a %d/%HZ')}", fontsize=8, fontweight='bold', loc='right')
        except Exception as e:
            plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[21].strftime('%a %d/%HZ')}", fontsize=8, fontweight='bold', loc='right')
        ax1.text(0.01, -0.08, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax1.text(0.8, -0.08, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
    
        wb = longitude - 6
        eb = longitude + 6
        nb = latitude + 3
        sb = latitude - 3
    
        ax2 = fig.add_subplot(gs[0:2, 8:10], projection=ccrs.PlateCarree())
        ax2.axis("off")
        ax2.set_extent([wb, eb, sb, nb], ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax2.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass    
    
        ax2.plot(longitude, latitude, marker='*', markersize=8, color='maroon', zorder=15)
        ax2.text(0.01, 0.01, "Reference System: "+reference_system, transform=ax2.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
    
        fig.savefig(f"{path}/{save_name}", bbox_inches='tight')
        plt.close(fig)
        print(f"Saved image of cross-section to {path_print}/{save_name}.")


    def plot_lower_atmosphere_temperature_rh_vertical_velocity_wind(model, station_id, save_name, longitude=None, latitude=None, data=False, ds=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-'):
    
        r'''
            This function plots a time vs. pressure cross-section forecast for a given point. Paramters: Lower Atmosphere Temperature/RH/Vertical Velocity/Wind. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) NAM - North American Model
                   3) RAP - RAP for the CONUS
                   4) RAP 32 - 32km North American RAP
    
            2) station_id (String) - The 4-letter airport station identifier. 
                                     If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

            3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                                    Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 
    
            Optional Arguments:
    
            1) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 
            
            2) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 
            
            3) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                and passing the data in or if the function needs to download the data. A value of False means the data
                is downloaded inside of the function while a value of True means the user is downloading the data outside
                of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                things, it is recommended to set this value to True and download the data outside of the function and pass
                it in so that the amount of data requests on the host servers can be minimized. 
    
    
            4) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 
    
            5) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                     wishes to use a reference system not on this list, please see items 17-23. 
                
                Reference Systems: 
                
                1) 'States & Counties'
                2) 'States Only'
                3) 'GACC Only'
                4) 'GACC & PSA'
                5) 'CWA Only'
                6) 'NWS CWAs & NWS Public Zones'
                7) 'NWS CWAs & NWS Fire Weather Zones'
                8) 'NWS CWAs & Counties'
                9) 'GACC & PSA & NWS Fire Weather Zones'
                10) 'GACC & PSA & NWS Public Zones'
                11) 'GACC & PSA & NWS CWA'
                12) 'GACC & PSA & Counties'
                13) 'GACC & Counties'
    
    
            6) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide state borders. 
    
            7) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide county borders. 
    
            8) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display GACC borders. 
    
            9) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display PSA borders.
    
            10) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display CWA borders.
    
            11) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.
    
            12) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.
    
            13) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 
    
            14) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 
    
            15) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 
    
            16) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 
    
            17) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 
    
            18) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 
    
            19) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 
    
            20) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 
    
            21) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                To change to a dashed line, users should set state_border_linestyle='--'. 
    
            22) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                To change to a dashed line, users should set county_border_linestyle='--'. 
    
            23) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                To change to a dashed line, users should set gacc_border_linestyle='--'. 
    
            24) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            25) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            26) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            27) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'.   
    
            Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}
        
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones
    
            state_border_linewidth = state_border_linewidth
            county_border_linewidth = county_border_linewidth
            gacc_border_linewidth = gacc_border_linewidth
            cwa_border_linewidth = cwa_border_linewidth
            nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
            nws_public_zones_linewidth = nws_public_zones_linewidth
            psa_border_linewidth = psa_border_linewidth
    
        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
                state_border_linewidth=1 
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                state_border_linewidth=1 
                county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
                gacc_border_linewidth=1
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
                cwa_border_linewidth=1
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                cwa_border_linewidth=1
                nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                cwa_border_linewidth=1
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                cwa_border_linewidth=1
                county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_public_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                cwa_border_linewidth=0.25
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                county_border_linewidth=0.25 
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                county_border_linewidth=0.25 

        if data == False:
            if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
                ds = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
                
                longitude = ds['tmpprs']['lon'].values
                latitude = ds['tmpprs']['lat'].values
        
            else:
                if model == 'RAP 32' or model == 'rap 32':
                    ds = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
                else:
                    ds = model_data.get_nomads_opendap_data_point_forecast(model, station_id, longitude, latitude)
                
                
        if data == True:
    
            ds = ds.squeeze()
    
            if station_id == 'Custom' or station_id == 'custom':
                longitude = longitude 
                latitude = latitude
                
            else:
                longitude, latitude = station_coords(station_id)
    
            if model == 'GFS0p25' or model == 'GFS0p50' or model == 'NA NAM' or model == 'RAP 32' or model == 'rap 32':
                
                if longitude < 0:
                    longitude = 360 + longitude
                else:
                    longitude = longitude   
            
            ds = ds.sel(lon=longitude, lat=latitude, method='nearest')
        ds = ds.sel(time=ds['time'][0:29])

        if model == 'NAM' or model == 'RAP' or model == 'RAP 32':
            ds = ds.sel(lev=ds['lev'][0:21])
        if model == 'GFS0p25':
            ds = ds.sel(lev=ds['lev'][0:13])
    
        if station_id == 'Custom' or station_id == 'custom':
            longitude = longitude
            latitude = latitude
    
        else:
            longitude = ds['tmpprs']['lon'].values
            latitude = ds['tmpprs']['lat'].values
    
        if longitude > 180:
            longitude = (360 - longitude) * -1
        else:
            longitude = longitude
    
    
        path, path_print = file_functions.forecast_cross_sections_graphics_paths(model, 'Time Cross Section', 'Lower Atmosphere Temperature & RH & Vertical Velocity & Wind Barbs', reference_system)
    
        try:
            os.remove(f"{path}/{save_name}")
        except Exception as e:
            pass
    
        print(f"The old {save_name} file in {path_print} has been deleted.")
    
        title_lon = str(round(float(abs(longitude)), 1))
        title_lat = str(round(float(abs(latitude)), 1))
    
        cmap = colormaps.vertical_velocity_colormap()
    
        u = (ds['ugrdprs']) * 2.23694
        v = (ds['vgrdprs']) * 2.23694
        vv = ds['vvelprs']
        
        time = ds['time']
        times = time.to_pandas()
        sfc_pressure = (ds['pressfc'][:]) / 100
        pressure = ds['ugrdprs']['lev']
        height_ft = (ds['hgtprs'][:, :]) * 3.28084
        height_sfc = (ds['hgtsfc'][:])  * 3.28084
        height_agl = height_ft - height_sfc
        pressure_grid, time_grid = np.meshgrid(pressure, time)
        temperature = ds['tmpprs'] - 273
        rh = ds['rhprs']
        lat = abs(round(float(ds['lat'].values), 1))
        lon = abs(round(float(ds['lon'].values), 1))
    
        if lon > 180:
            lon = 360 - lon
        else:
            lon = lon
    
        if lat >= 0:
            lat_symbol = '°N'
        else:
            lat_symbol = '°S'
    
        if lon <= 180:
            lon_symbol = '°W'
        else:
            lon_symbol = '°E'
        
        
        fig = plt.figure(figsize=(18, 7))
        fig.set_facecolor('aliceblue')
        gs = gridspec.GridSpec(10, 10)
    
        ax1 = fig.add_subplot(gs[0:10, 0:10])
        
        ax1.set_yscale('symlog')
        ax1.set_yticks(np.arange(1000, 50, -100))
        ax1.set_yticklabels(np.arange(1000, 50, -100))
        ax1.set_ylim(np.nanmax(sfc_pressure), 475)
        ax1.xaxis.set_major_formatter(md.DateFormatter('%d/%HZ'))
        ax1.set_xticks(time)

        low = np.nanmin(vv[:, :])
        high = np.nanmax(vv[:, :])

        if low < 0 and high >= 0:
            vv_range = abs(low) + high
        if low < 0 and high < 0 :
            vv_range = low - high
        if low >= 0 and high >= 0:
            vv_range = high - low

        step = round(vv_range/10, 1)

        if low < 0 and abs(low) > high and high >=0:
            upper_bound = round(abs(low),2)
            lower_bound = round(low,2)
        if low < 0 and high >= 0 and abs(low) <= high:
            lower_bound = round((high * -1),2)
            upper_bound = round(high,2)
        if low < 0 and high < 0:
            upper_bound = round(high,2)
            lower_bound = round(low,2)
        if low >= 0 and high >= 0:
            upper_bound = round(high,2)
            lower_bound = round(low,2)
        
        step_cs = round(vv_range/100, 2)

        step_c = 3
        start_c = round(np.nanmin(temperature),0)
        stop_c = (round(np.nanmax(temperature),0) + step_c)
                            
        ax1.contourf(time_grid, pressure_grid, vv[:, :], levels=np.arange(lower_bound, (upper_bound + step_cs), step_cs), cmap=cmap, alpha=0.25, extend='both')
        c = ax1.contour(time_grid, pressure_grid, temperature, levels = np.arange(start_c, (stop_c + step_c), step_c), colors='black', zorder=2, linewidths=1, linestyles='-')
        ax1.clabel(c, levels = np.arange(start_c, (stop_c + step_c), step_c), inline=True, fontsize=8, rightside_up=True)
        c1 = ax1.contour(time_grid, pressure_grid, rh, levels = np.arange(0, 110, 10), colors='green', zorder=2, linewidths=1, linestyles='--')
        ax1.clabel(c1, levels = np.arange(0, 110, 10), inline=True, fontsize=8, rightside_up=True)  
        c2 = ax1.contour(time_grid, pressure_grid, temperature, levels=[-18,-12], colors='black', zorder=2, linewidths=1, linestyles='dotted')
        ax1.clabel(c2, levels=[-18,-12], inline=True, fontsize=8, rightside_up=True)
        ax1.barbs(time_grid, pressure_grid, u[:, :], v[:, :], clip_on=True, zorder=10, color='black', length=5, alpha=0.5)
        if station_id != 'Custom' or station_id != 'custom':
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: VERTICAL VELOCITY (SHADED) [Pa/s] & T [°C] (SOLID CONTOURS) & RH [%] (DASHED CONTOURS) & WIND BARBS [MPH]\nSTATION: {station_id.upper()} - LAT: {str(round(lat,1))}{lat_symbol} | LON: {str(round(lon,1))}{lon_symbol}", fontsize=9, fontweight='bold', loc='left')
        else:
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: VERTICAL VELOCITY (SHADED) [Pa/s] & T [°C] (SOLID CONTOURS) & RH [%] (DASHED CONTOURS) & WIND BARBS [MPH]\nLAT: {str(round(lat,1))}{lat_symbol} | LON: {str(round(lon,1))}{lon_symbol}", fontsize=9, fontweight='bold', loc='left')
        try:
            plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[28].strftime('%a %d/%HZ')}", fontsize=8, fontweight='bold', loc='right')
        except Exception as e:
            plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[21].strftime('%a %d/%HZ')}", fontsize=8, fontweight='bold', loc='right')
        ax1.text(0.01, -0.08, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax1.text(0.8, -0.08, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
    
        wb = longitude - 6
        eb = longitude + 6
        nb = latitude + 3
        sb = latitude - 3
    
        ax2 = fig.add_subplot(gs[0:2, 8:10], projection=ccrs.PlateCarree())
        ax2.axis("off")
        ax2.set_extent([wb, eb, sb, nb], ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax2.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass    
    
        ax2.plot(longitude, latitude, marker='*', markersize=8, color='maroon', zorder=15)
        ax2.text(0.01, 0.01, "Reference System: "+reference_system, transform=ax2.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
    
        fig.savefig(f"{path}/{save_name}", bbox_inches='tight')
        plt.close(fig)
        print(f"Saved image of cross-section to {path_print}/{save_name}.")


    def plot_lower_atmosphere_temperature_and_wind(model, station_id, save_name, longitude=None, latitude=None, data=False, ds=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-'):
    
        r'''
            This function plots a time vs. pressure cross-section forecast for a given point. Paramters: Lower Atmosphere Temperature/Wind. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) NAM - North American Model
                   3) RAP - RAP for the CONUS
                   4) RAP 32 - 32km North American RAP
    
            2) station_id (String) - The 4-letter airport station identifier. 
                                     If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

            3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                                    Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 
    
            Optional Arguments:
    
            1) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 
            
            2) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 
            
            3) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                and passing the data in or if the function needs to download the data. A value of False means the data
                is downloaded inside of the function while a value of True means the user is downloading the data outside
                of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                things, it is recommended to set this value to True and download the data outside of the function and pass
                it in so that the amount of data requests on the host servers can be minimized. 
    
    
            4) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 
    
            5) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                     wishes to use a reference system not on this list, please see items 17-23. 
                
                Reference Systems: 
                
                1) 'States & Counties'
                2) 'States Only'
                3) 'GACC Only'
                4) 'GACC & PSA'
                5) 'CWA Only'
                6) 'NWS CWAs & NWS Public Zones'
                7) 'NWS CWAs & NWS Fire Weather Zones'
                8) 'NWS CWAs & Counties'
                9) 'GACC & PSA & NWS Fire Weather Zones'
                10) 'GACC & PSA & NWS Public Zones'
                11) 'GACC & PSA & NWS CWA'
                12) 'GACC & PSA & Counties'
                13) 'GACC & Counties'
    
    
            6) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide state borders. 
    
            7) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide county borders. 
    
            8) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display GACC borders. 
    
            9) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display PSA borders.
    
            10) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display CWA borders.
    
            11) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.
    
            12) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.
    
            13) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 
    
            14) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 
    
            15) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 
    
            16) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 
    
            17) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 
    
            18) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 
    
            19) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 
    
            20) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 
    
            21) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                To change to a dashed line, users should set state_border_linestyle='--'. 
    
            22) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                To change to a dashed line, users should set county_border_linestyle='--'. 
    
            23) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                To change to a dashed line, users should set gacc_border_linestyle='--'. 
    
            24) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            25) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            26) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            27) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'.   
    
            Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones
    
            state_border_linewidth = state_border_linewidth
            county_border_linewidth = county_border_linewidth
            gacc_border_linewidth = gacc_border_linewidth
            cwa_border_linewidth = cwa_border_linewidth
            nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
            nws_public_zones_linewidth = nws_public_zones_linewidth
            psa_border_linewidth = psa_border_linewidth
    
        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
                state_border_linewidth=1 
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                state_border_linewidth=1 
                county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
                gacc_border_linewidth=1
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
                cwa_border_linewidth=1
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                cwa_border_linewidth=1
                nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                cwa_border_linewidth=1
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                cwa_border_linewidth=1
                county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_public_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                cwa_border_linewidth=0.25
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                county_border_linewidth=0.25 
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                county_border_linewidth=0.25 

        if data == False:
            if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
                ds = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
                
                longitude = ds['tmpprs']['lon'].values
                latitude = ds['tmpprs']['lat'].values
        
            else:
                if model == 'RAP 32' or model == 'rap 32':
                    ds = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
                else:
                    ds = model_data.get_nomads_opendap_data_point_forecast(model, station_id, longitude, latitude)
                
                
        if data == True:
    
            ds = ds.squeeze()
    
            if station_id == 'Custom' or station_id == 'custom':
                longitude = longitude 
                latitude = latitude
                
            else:
                longitude, latitude = station_coords(station_id)
    
            if model == 'GFS0p25' or model == 'GFS0p50' or model == 'NA NAM' or model == 'RAP 32' or model == 'rap 32':
                
                if longitude < 0:
                    longitude = 360 + longitude
                else:
                    longitude = longitude   
            
            ds = ds.sel(lon=longitude, lat=latitude, method='nearest')
        ds = ds.sel(time=ds['time'][0:29])

        if model == 'NAM' or model == 'RAP' or model == 'RAP 32':
            ds = ds.sel(lev=ds['lev'][0:21])
        if model == 'GFS0p25':
            ds = ds.sel(lev=ds['lev'][0:13])
    
        if station_id == 'Custom' or station_id == 'custom':
            longitude = longitude
            latitude = latitude
    
        else:
            longitude = ds['tmpprs']['lon'].values
            latitude = ds['tmpprs']['lat'].values
    
        if longitude > 180:
            longitude = (360 - longitude) * -1
        else:
            longitude = longitude
    
    
        path, path_print = file_functions.forecast_cross_sections_graphics_paths(model, 'Time Cross Section', 'Lower Atmosphere Temperature & Wind Barbs', reference_system)
    
        try:
            os.remove(f"{path}/{save_name}")
        except Exception as e:
            pass
    
        print(f"The old {save_name} file in {path_print} has been deleted.")
    
        title_lon = str(round(float(abs(longitude)), 1))
        title_lat = str(round(float(abs(latitude)), 1))
    
        cmap = colormaps.temperature_colormap()
    
        u = (ds['ugrdprs']) * 2.23694
        v = (ds['vgrdprs']) * 2.23694
        
        time = ds['time']
        times = time.to_pandas()
        sfc_pressure = (ds['pressfc'][:]) / 100
        pressure = ds['ugrdprs']['lev']
        height_ft = (ds['hgtprs'][:, :]) * 3.28084
        height_sfc = (ds['hgtsfc'][:])  * 3.28084
        height_agl = height_ft - height_sfc
        pressure_grid, time_grid = np.meshgrid(pressure, time)
        temperature = ds['tmpprs'] - 273.15
        lat = abs(round(float(ds['lat'].values), 1))
        lon = abs(round(float(ds['lon'].values), 1))
    
        if lon > 180:
            lon = 360 - lon
        else:
            lon = lon
    
        if lat >= 0:
            lat_symbol = '°N'
        else:
            lat_symbol = '°S'
    
        if lon <= 180:
            lon_symbol = '°W'
        else:
            lon_symbol = '°E'
        
        
        fig = plt.figure(figsize=(18, 7))
        fig.set_facecolor('aliceblue')
        gs = gridspec.GridSpec(10, 10)
    
        ax1 = fig.add_subplot(gs[0:10, 0:10])
        
        ax1.set_yscale('symlog')
        ax1.set_yticks(np.arange(1000, 50, -100))
        ax1.set_yticklabels(np.arange(1000, 50, -100))
        ax1.set_ylim(np.nanmax(sfc_pressure), 475)
        ax1.xaxis.set_major_formatter(md.DateFormatter('%d/%HZ'))
        ax1.set_xticks(time)

        step_cs = 0.1
        low = round(np.nanmin(temperature),1)
        high = round(np.nanmax(temperature),1)

        step_c = 3
        start_c = round(np.nanmin(temperature),0)
        stop_c = (round(np.nanmax(temperature),0) + step_c)

        if low < 0 and abs(low) > high and high >=0:
            upper_bound = round(abs(low),2)
            lower_bound = round(low,2)
        if low < 0 and high >= 0 and abs(low) <= high:
            lower_bound = round((high * -1),2)
            upper_bound = round(high,2)
        if low < 0 and high < 0:
            upper_bound = round(high,2)
            lower_bound = round(low,2)
        if low >= 0 and high >= 0:
            upper_bound = round(high,2)
            lower_bound = round(low,2)
        
        
        ax1.contourf(time_grid, pressure_grid, temperature, levels=np.arange(lower_bound, (upper_bound + step_cs), step_cs), cmap=cmap, alpha=0.25, extend='both')
        c = ax1.contour(time_grid, pressure_grid, temperature, levels = np.arange(start_c, stop_c, step_c), colors='black', zorder=2, linewidths=1, linestyles='--')
        ax1.clabel(c, levels = np.arange(start_c, stop_c, step_c), inline=True, fontsize=8, rightside_up=True)
        ax1.barbs(time_grid, pressure_grid, u[:, :], v[:, :], clip_on=True, zorder=10, color='black', length=5, alpha=0.5)
        if station_id != 'Custom' or station_id != 'custom':
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: TEMPERATURE [°C] & WIND BARBS [MPH]\nSTATION: {station_id.upper()} - LAT: {str(round(lat,1))}{lat_symbol} | LON: {str(round(lon,1))}{lon_symbol}", fontsize=10, fontweight='bold', loc='left')
        else:
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: TEMPERATURE [°C] & WIND BARBS [MPH]\nLAT: {str(round(lat,1))}{lat_symbol} | LON: {str(round(lon,1))}{lon_symbol}", fontsize=10, fontweight='bold', loc='left')
        try:
            plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[28].strftime('%a %d/%HZ')}", fontsize=8, fontweight='bold', loc='right')
        except Exception as e:
            plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[21].strftime('%a %d/%HZ')}", fontsize=8, fontweight='bold', loc='right')
        ax1.text(0.01, -0.08, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax1.text(0.8, -0.08, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
    
        wb = longitude - 6
        eb = longitude + 6
        nb = latitude + 3
        sb = latitude - 3
    
        ax2 = fig.add_subplot(gs[0:2, 8:10], projection=ccrs.PlateCarree())
        ax2.axis("off")
        ax2.set_extent([wb, eb, sb, nb], ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax2.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass    
    
        ax2.plot(longitude, latitude, marker='*', markersize=8, color='maroon', zorder=15)
        ax2.text(0.01, 0.01, "Reference System: "+reference_system, transform=ax2.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
    
        fig.savefig(f"{path}/{save_name}", bbox_inches='tight')
        plt.close(fig)
        print(f"Saved image of cross-section to {path_print}/{save_name}.")


    def plot_lower_atmosphere_relative_humidity_and_wind(model, station_id, save_name, longitude=None, latitude=None, data=False, ds=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-'):
    
        r'''
            This function plots a time vs. pressure cross-section forecast for a given point. Paramters: Lower Atmosphere RH/Wind. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) NAM - North American Model
                   3) RAP - RAP for the CONUS
                   4) RAP 32 - 32km North American RAP
    
            2) station_id (String) - The 4-letter airport station identifier. 
                                     If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

            3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                                    Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 
    
            Optional Arguments:
    
            1) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 
            
            2) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 
            
            3) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                and passing the data in or if the function needs to download the data. A value of False means the data
                is downloaded inside of the function while a value of True means the user is downloading the data outside
                of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                things, it is recommended to set this value to True and download the data outside of the function and pass
                it in so that the amount of data requests on the host servers can be minimized. 
    
    
            4) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 
    
            5) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                     wishes to use a reference system not on this list, please see items 17-23. 
                
                Reference Systems: 
                
                1) 'States & Counties'
                2) 'States Only'
                3) 'GACC Only'
                4) 'GACC & PSA'
                5) 'CWA Only'
                6) 'NWS CWAs & NWS Public Zones'
                7) 'NWS CWAs & NWS Fire Weather Zones'
                8) 'NWS CWAs & Counties'
                9) 'GACC & PSA & NWS Fire Weather Zones'
                10) 'GACC & PSA & NWS Public Zones'
                11) 'GACC & PSA & NWS CWA'
                12) 'GACC & PSA & Counties'
                13) 'GACC & Counties'
    
    
            6) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide state borders. 
    
            7) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide county borders. 
    
            8) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display GACC borders. 
    
            9) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display PSA borders.
    
            10) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display CWA borders.
    
            11) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.
    
            12) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.
    
            13) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 
    
            14) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 
    
            15) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 
    
            16) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 
    
            17) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 
    
            18) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 
    
            19) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 
    
            20) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 
    
            21) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                To change to a dashed line, users should set state_border_linestyle='--'. 
    
            22) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                To change to a dashed line, users should set county_border_linestyle='--'. 
    
            23) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                To change to a dashed line, users should set gacc_border_linestyle='--'. 
    
            24) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            25) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            26) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            27) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'.   
    
            Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}
        
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones
    
            state_border_linewidth = state_border_linewidth
            county_border_linewidth = county_border_linewidth
            gacc_border_linewidth = gacc_border_linewidth
            cwa_border_linewidth = cwa_border_linewidth
            nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
            nws_public_zones_linewidth = nws_public_zones_linewidth
            psa_border_linewidth = psa_border_linewidth
    
        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
                state_border_linewidth=1 
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                state_border_linewidth=1 
                county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
                gacc_border_linewidth=1
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
                cwa_border_linewidth=1
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                cwa_border_linewidth=1
                nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                cwa_border_linewidth=1
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                cwa_border_linewidth=1
                county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_public_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                cwa_border_linewidth=0.25
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                county_border_linewidth=0.25 
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                county_border_linewidth=0.25 

        if data == False:
            if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
                ds = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
                
                longitude = ds['tmpprs']['lon'].values
                latitude = ds['tmpprs']['lat'].values
        
            else:
                if model == 'RAP 32' or model == 'rap 32':
                    ds = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
                else:
                    ds = model_data.get_nomads_opendap_data_point_forecast(model, station_id, longitude, latitude)
                
                
        if data == True:
    
            ds = ds.squeeze()
    
            if station_id == 'Custom' or station_id == 'custom':
                longitude = longitude 
                latitude = latitude
                
            else:
                longitude, latitude = station_coords(station_id)
    
            if model == 'GFS0p25' or model == 'GFS0p50' or model == 'NA NAM' or model == 'RAP 32' or model == 'rap 32':
                
                if longitude < 0:
                    longitude = 360 + longitude
                else:
                    longitude = longitude   
            
            ds = ds.sel(lon=longitude, lat=latitude, method='nearest')
        ds = ds.sel(time=ds['time'][0:29])

        if model == 'NAM' or model == 'RAP' or model == 'RAP 32':
            ds = ds.sel(lev=ds['lev'][0:21])
        if model == 'GFS0p25':
            ds = ds.sel(lev=ds['lev'][0:13])
    
        if station_id == 'Custom' or station_id == 'custom':
            longitude = longitude
            latitude = latitude
    
        else:
            longitude = ds['tmpprs']['lon'].values
            latitude = ds['tmpprs']['lat'].values
    
        if longitude > 180:
            longitude = (360 - longitude) * -1
        else:
            longitude = longitude
    
    
        path, path_print = file_functions.forecast_cross_sections_graphics_paths(model, 'Time Cross Section', 'Lower Atmosphere RH & Wind Barbs', reference_system)
    
        try:
            os.remove(f"{path}/{save_name}")
        except Exception as e:
            pass
    
        print(f"The old {save_name} file in {path_print} has been deleted.")
    
        title_lon = str(round(float(abs(longitude)), 1))
        title_lat = str(round(float(abs(latitude)), 1))
    
        cmap = colormaps.relative_humidity_colormap()
    
        u = (ds['ugrdprs']) * 2.23694
        v = (ds['vgrdprs']) * 2.23694
        
        time = ds['time']
        times = time.to_pandas()
        sfc_pressure = (ds['pressfc'][:]) / 100
        pressure = ds['ugrdprs']['lev']
        height_ft = (ds['hgtprs'][:, :]) * 3.28084
        height_sfc = (ds['hgtsfc'][:])  * 3.28084
        height_agl = height_ft - height_sfc
        pressure_grid, time_grid = np.meshgrid(pressure, time)
        rh = ds['rhprs']
        lat = abs(round(float(ds['lat'].values), 1))
        lon = abs(round(float(ds['lon'].values), 1))
    
        if lon > 180:
            lon = 360 - lon
        else:
            lon = lon
    
        if lat >= 0:
            lat_symbol = '°N'
        else:
            lat_symbol = '°S'
    
        if lon <= 180:
            lon_symbol = '°W'
        else:
            lon_symbol = '°E'
        
        
        fig = plt.figure(figsize=(18, 7))
        fig.set_facecolor('aliceblue')
        gs = gridspec.GridSpec(10, 10)
    
        ax1 = fig.add_subplot(gs[0:10, 0:10])
        
        ax1.set_yscale('symlog')
        ax1.set_yticks(np.arange(1000, 50, -100))
        ax1.set_yticklabels(np.arange(1000, 50, -100))
        ax1.set_ylim(np.nanmax(sfc_pressure), 475)
        ax1.xaxis.set_major_formatter(md.DateFormatter('%d/%HZ'))
        ax1.set_xticks(time)
      
        
        ax1.contourf(time_grid, pressure_grid, rh, levels=np.arange(0, 102, 1), cmap=cmap, alpha=0.25, extend='both')
        c = ax1.contour(time_grid, pressure_grid, rh, levels = np.arange(0, 110, 10), colors='blue', zorder=2, linewidths=1, linestyles='--')
        ax1.clabel(c, levels = np.arange(0, 110, 10), inline=True, fontsize=8, rightside_up=True)
        ax1.barbs(time_grid, pressure_grid, u[:, :], v[:, :], clip_on=True, zorder=10, color='black', length=5, alpha=0.5)
        if station_id != 'Custom' or station_id != 'custom':
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: RELATIVE HUMIDITY [%] & WIND BARBS [MPH]\nSTATION: {station_id.upper()} - LAT: {str(round(lat,1))}{lat_symbol} | LON: {str(round(lon,1))}{lon_symbol}", fontsize=10, fontweight='bold', loc='left')
        else:
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: RELATIVE HUMIDITY [%] & WIND BARBS [MPH]\nLAT: {str(round(lat,1))}{lat_symbol} | LON: {str(round(lon,1))}{lon_symbol}", fontsize=10, fontweight='bold', loc='left')
        try:
            plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[28].strftime('%a %d/%HZ')}", fontsize=8, fontweight='bold', loc='right')
        except Exception as e:
            plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[21].strftime('%a %d/%HZ')}", fontsize=8, fontweight='bold', loc='right')
        ax1.text(0.01, -0.08, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax1.text(0.8, -0.08, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
    
        wb = longitude - 6
        eb = longitude + 6
        nb = latitude + 3
        sb = latitude - 3
    
        ax2 = fig.add_subplot(gs[0:2, 8:10], projection=ccrs.PlateCarree())
        ax2.axis("off")
        ax2.set_extent([wb, eb, sb, nb], ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax2.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass    
    
        ax2.plot(longitude, latitude, marker='*', markersize=8, color='maroon', zorder=15)
        ax2.text(0.01, 0.01, "Reference System: "+reference_system, transform=ax2.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
    
        fig.savefig(f"{path}/{save_name}", bbox_inches='tight')
        plt.close(fig)
        print(f"Saved image of cross-section to {path_print}/{save_name}.")


    def plot_lower_atmosphere_theta_e_and_wind(model, station_id, save_name, longitude=None, latitude=None, data=False, ds=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-'):
    
        r'''
            This function plots a time vs. pressure cross-section forecast for a given point. Paramters: Lower Atmosphere Theta-E/Wind. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) NAM - North American Model
                   3) RAP - RAP for the CONUS
                   4) RAP 32 - 32km North American RAP
    
            2) station_id (String) - The 4-letter airport station identifier. 
                                     If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

            3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                                    Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 
    
            Optional Arguments:
    
            1) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 
            
            2) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 
            
            3) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                and passing the data in or if the function needs to download the data. A value of False means the data
                is downloaded inside of the function while a value of True means the user is downloading the data outside
                of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                things, it is recommended to set this value to True and download the data outside of the function and pass
                it in so that the amount of data requests on the host servers can be minimized. 
    
    
            4) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 
    
            5) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                     wishes to use a reference system not on this list, please see items 17-23. 
                
                Reference Systems: 
                
                1) 'States & Counties'
                2) 'States Only'
                3) 'GACC Only'
                4) 'GACC & PSA'
                5) 'CWA Only'
                6) 'NWS CWAs & NWS Public Zones'
                7) 'NWS CWAs & NWS Fire Weather Zones'
                8) 'NWS CWAs & Counties'
                9) 'GACC & PSA & NWS Fire Weather Zones'
                10) 'GACC & PSA & NWS Public Zones'
                11) 'GACC & PSA & NWS CWA'
                12) 'GACC & PSA & Counties'
                13) 'GACC & Counties'
    
    
            6) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide state borders. 
    
            7) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide county borders. 
    
            8) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display GACC borders. 
    
            9) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display PSA borders.
    
            10) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display CWA borders.
    
            11) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.
    
            12) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.
    
            13) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 
    
            14) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 
    
            15) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 
    
            16) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 
    
            17) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 
    
            18) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 
    
            19) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 
    
            20) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 
    
            21) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                To change to a dashed line, users should set state_border_linestyle='--'. 
    
            22) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                To change to a dashed line, users should set county_border_linestyle='--'. 
    
            23) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                To change to a dashed line, users should set gacc_border_linestyle='--'. 
    
            24) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            25) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            26) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            27) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'.   
    
            Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}
        
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones
    
            state_border_linewidth = state_border_linewidth
            county_border_linewidth = county_border_linewidth
            gacc_border_linewidth = gacc_border_linewidth
            cwa_border_linewidth = cwa_border_linewidth
            nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
            nws_public_zones_linewidth = nws_public_zones_linewidth
            psa_border_linewidth = psa_border_linewidth
    
        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
                state_border_linewidth=1 
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                state_border_linewidth=1 
                county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
                gacc_border_linewidth=1
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
                cwa_border_linewidth=1
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                cwa_border_linewidth=1
                nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                cwa_border_linewidth=1
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                cwa_border_linewidth=1
                county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_public_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                cwa_border_linewidth=0.25
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                county_border_linewidth=0.25 
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                county_border_linewidth=0.25 

        if data == False:
            if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
                ds = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
                
                longitude = ds['tmpprs']['lon'].values
                latitude = ds['tmpprs']['lat'].values
        
            else:
                if model == 'RAP 32' or model == 'rap 32':
                    ds = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
                else:
                    ds = model_data.get_nomads_opendap_data_point_forecast(model, station_id, longitude, latitude)
                
                
        if data == True:
    
            ds = ds.squeeze()
    
            if station_id == 'Custom' or station_id == 'custom':
                longitude = longitude 
                latitude = latitude
                
            else:
                longitude, latitude = station_coords(station_id)
    
            if model == 'GFS0p25' or model == 'GFS0p50' or model == 'NA NAM' or model == 'RAP 32' or model == 'rap 32':
                
                if longitude < 0:
                    longitude = 360 + longitude
                else:
                    longitude = longitude   
            
            ds = ds.sel(lon=longitude, lat=latitude, method='nearest')
        ds = ds.sel(time=ds['time'][0:29])

        if model == 'NAM' or model == 'RAP' or model == 'RAP 32':
            ds = ds.sel(lev=ds['lev'][0:21])
        if model == 'GFS0p25':
            ds = ds.sel(lev=ds['lev'][0:13])
    
        if station_id == 'Custom' or station_id == 'custom':
            longitude = longitude
            latitude = latitude
    
        else:
            longitude = ds['tmpprs']['lon'].values
            latitude = ds['tmpprs']['lat'].values
    
        if longitude > 180:
            longitude = (360 - longitude) * -1
        else:
            longitude = longitude
    
    
        path, path_print = file_functions.forecast_cross_sections_graphics_paths(model, 'Time Cross Section', 'Lower Atmosphere Theta E & Wind Barbs', reference_system)
    
        try:
            os.remove(f"{path}/{save_name}")
        except Exception as e:
            pass
    
        print(f"The old {save_name} file in {path_print} has been deleted.")
    
        title_lon = str(round(float(abs(longitude)), 1))
        title_lat = str(round(float(abs(latitude)), 1))
    
        cmap = colormaps.theta_e_colormap()
    
        u = (ds['ugrdprs']) * 2.23694
        v = (ds['vgrdprs']) * 2.23694
        
        time = ds['time']
        times = time.to_pandas()
        sfc_pressure = (ds['pressfc'][:]) / 100
        pressure = ds['ugrdprs']['lev']
        height_ft = (ds['hgtprs'][:, :]) * 3.28084
        height_sfc = (ds['hgtsfc'][:])  * 3.28084
        height_agl = height_ft - height_sfc
        pressure_grid, time_grid = np.meshgrid(pressure, time)
        ds['dwptprs'] = mpcalc.dewpoint_from_relative_humidity(ds['tmpprs'] * units('kelvin'), ds['rhprs'] * units('percent'))
        theta_e = mpcalc.equivalent_potential_temperature(ds['lev'] * units('hPa'), ds['tmpprs'] * units('kelvin'), ds['dwptprs']) 
        theta_e = theta_e.to_numpy()
        if model == 'NAM':
            theta_e = theta_e.reshape(29,21)
        if model == 'GFS0p25':
            theta_e = theta_e.reshape(29,13)
        if model == 'RAP':
            theta_e = theta_e.reshape(22,21)
        lat = abs(round(float(ds['lat'].values), 1))
        lon = abs(round(float(ds['lon'].values), 1))
    
        if lon > 180:
            lon = 360 - lon
        else:
            lon = lon
    
        if lat >= 0:
            lat_symbol = '°N'
        else:
            lat_symbol = '°S'
    
        if lon <= 180:
            lon_symbol = '°W'
        else:
            lon_symbol = '°E'
        
        
        fig = plt.figure(figsize=(18, 7))
        fig.set_facecolor('aliceblue')
        gs = gridspec.GridSpec(10, 10)
    
        ax1 = fig.add_subplot(gs[0:10, 0:10])
        
        ax1.set_yscale('symlog')
        ax1.set_yticks(np.arange(1000, 50, -100))
        ax1.set_yticklabels(np.arange(1000, 50, -100))
        ax1.set_ylim(np.nanmax(sfc_pressure), 475)
        ax1.xaxis.set_major_formatter(md.DateFormatter('%d/%HZ'))
        ax1.set_xticks(time)

        lower_bound = int(round(np.nanmin(theta_e), 0))
        upper_bound = int(round(np.nanmax(theta_e), 0))
        step_cs = 1
        step_c = 3
        
        ax1.contourf(time_grid, pressure_grid, theta_e, levels=np.arange(lower_bound, (upper_bound + step_cs), step_cs), cmap=cmap, alpha=0.25, extend='both')
        c = ax1.contour(time_grid, pressure_grid, theta_e, levels = np.arange(lower_bound, (upper_bound + step_c), step_c), colors='black', zorder=2, linewidths=1, linestyles='--')
        ax1.clabel(c, levels = np.arange(lower_bound, (upper_bound + step_c), step_c), inline=True, fontsize=8, rightside_up=True)
        ax1.barbs(time_grid, pressure_grid, u[:, :], v[:, :], clip_on=True, zorder=10, color='black', length=5, alpha=0.5)
        if station_id != 'Custom' or station_id != 'custom':
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: THETA-E [K] & WIND BARBS [MPH]\nSTATION: {station_id.upper()} - LAT: {str(round(lat,1))}{lat_symbol} | LON: {str(round(lon,1))}{lon_symbol}", fontsize=10, fontweight='bold', loc='left')
        else:
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: THETA-E [K] & WIND BARBS [MPH]\nLAT: {str(round(lat,1))}{lat_symbol} | LON: {str(round(lon,1))}{lon_symbol}", fontsize=10, fontweight='bold', loc='left')

        try:
            plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[28].strftime('%a %d/%HZ')}", fontsize=8, fontweight='bold', loc='right')
        except Exception as e:
            plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[21].strftime('%a %d/%HZ')}", fontsize=8, fontweight='bold', loc='right')
        ax1.text(0.01, -0.08, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax1.text(0.8, -0.08, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
    
        wb = longitude - 6
        eb = longitude + 6
        nb = latitude + 3
        sb = latitude - 3
    
        ax2 = fig.add_subplot(gs[0:2, 8:10], projection=ccrs.PlateCarree())
        ax2.axis("off")
        ax2.set_extent([wb, eb, sb, nb], ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax2.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass    
    
        ax2.plot(longitude, latitude, marker='*', markersize=8, color='maroon', zorder=15)
        ax2.text(0.01, 0.01, "Reference System: "+reference_system, transform=ax2.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
    
        fig.savefig(f"{path}/{save_name}", bbox_inches='tight')
        plt.close(fig)
        print(f"Saved image of cross-section to {path_print}/{save_name}.")
        

    def plot_lower_atmosphere_theta_e_rh_vertical_velocity_wind(model, station_id, save_name, longitude=None, latitude=None, data=False, ds=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-'):
    
        r'''
             This function plots a time vs. pressure cross-section forecast for a given point. Paramters: Lower Atmosphere Theta-E/RH/Vertical Velocity/Wind. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) NAM - North American Model
                   3) RAP - RAP for the CONUS
                   4) RAP 32 - 32km North American RAP
    
            2) station_id (String) - The 4-letter airport station identifier. 
                                     If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

            3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                                    Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 
    
            Optional Arguments:
    
            1) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 
            
            2) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 
            
            3) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                and passing the data in or if the function needs to download the data. A value of False means the data
                is downloaded inside of the function while a value of True means the user is downloading the data outside
                of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                things, it is recommended to set this value to True and download the data outside of the function and pass
                it in so that the amount of data requests on the host servers can be minimized. 
    
    
            4) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 
    
            5) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                     wishes to use a reference system not on this list, please see items 17-23. 
                
                Reference Systems: 
                
                1) 'States & Counties'
                2) 'States Only'
                3) 'GACC Only'
                4) 'GACC & PSA'
                5) 'CWA Only'
                6) 'NWS CWAs & NWS Public Zones'
                7) 'NWS CWAs & NWS Fire Weather Zones'
                8) 'NWS CWAs & Counties'
                9) 'GACC & PSA & NWS Fire Weather Zones'
                10) 'GACC & PSA & NWS Public Zones'
                11) 'GACC & PSA & NWS CWA'
                12) 'GACC & PSA & Counties'
                13) 'GACC & Counties'
    
    
            6) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide state borders. 
    
            7) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide county borders. 
    
            8) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display GACC borders. 
    
            9) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display PSA borders.
    
            10) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display CWA borders.
    
            11) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.
    
            12) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.
    
            13) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 
    
            14) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 
    
            15) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 
    
            16) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 
    
            17) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 
    
            18) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 
    
            19) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 
    
            20) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 
    
            21) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                To change to a dashed line, users should set state_border_linestyle='--'. 
    
            22) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                To change to a dashed line, users should set county_border_linestyle='--'. 
    
            23) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                To change to a dashed line, users should set gacc_border_linestyle='--'. 
    
            24) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            25) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            26) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            27) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'.   
    
            Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones
    
            state_border_linewidth = state_border_linewidth
            county_border_linewidth = county_border_linewidth
            gacc_border_linewidth = gacc_border_linewidth
            cwa_border_linewidth = cwa_border_linewidth
            nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
            nws_public_zones_linewidth = nws_public_zones_linewidth
            psa_border_linewidth = psa_border_linewidth
    
        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
                state_border_linewidth=1 
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                state_border_linewidth=1 
                county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
                gacc_border_linewidth=1
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
                cwa_border_linewidth=1
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                cwa_border_linewidth=1
                nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                cwa_border_linewidth=1
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                cwa_border_linewidth=1
                county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_public_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                cwa_border_linewidth=0.25
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                county_border_linewidth=0.25 
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                county_border_linewidth=0.25 

        if data == False:
            if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
                ds = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
                
                longitude = ds['tmpprs']['lon'].values
                latitude = ds['tmpprs']['lat'].values
        
            else:
                if model == 'RAP 32' or model == 'rap 32':
                    ds = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
                else:
                    ds = model_data.get_nomads_opendap_data_point_forecast(model, station_id, longitude, latitude)
                
                
        if data == True:
    
            ds = ds.squeeze()
    
            if station_id == 'Custom' or station_id == 'custom':
                longitude = longitude 
                latitude = latitude
                
            else:
                longitude, latitude = station_coords(station_id)
    
            if model == 'GFS0p25' or model == 'GFS0p50' or model == 'NA NAM' or model == 'RAP 32' or model == 'rap 32':
                
                if longitude < 0:
                    longitude = 360 + longitude
                else:
                    longitude = longitude   
            
            ds = ds.sel(lon=longitude, lat=latitude, method='nearest')
        ds = ds.sel(time=ds['time'][0:29])

        if model == 'NAM' or model == 'RAP' or model == 'RAP 32':
            ds = ds.sel(lev=ds['lev'][0:21])
        if model == 'GFS0p25':
            ds = ds.sel(lev=ds['lev'][0:13])
    
        if station_id == 'Custom' or station_id == 'custom':
            longitude = longitude
            latitude = latitude
    
        else:
            longitude = ds['tmpprs']['lon'].values
            latitude = ds['tmpprs']['lat'].values
    
        if longitude > 180:
            longitude = (360 - longitude) * -1
        else:
            longitude = longitude
    
    
        path, path_print = file_functions.forecast_cross_sections_graphics_paths(model, 'Time Cross Section', 'Lower Atmosphere Theta E & RH & Vertical Velocity & Wind Barbs', reference_system)
    
        try:
            os.remove(f"{path}/{save_name}")
        except Exception as e:
            pass
    
        print(f"The old {save_name} file in {path_print} has been deleted.")
    
        title_lon = str(round(float(abs(longitude)), 1))
        title_lat = str(round(float(abs(latitude)), 1))
    
        cmap = colormaps.vertical_velocity_colormap()
    
        u = (ds['ugrdprs']) * 2.23694
        v = (ds['vgrdprs']) * 2.23694
        vv = ds['vvelprs']
        
        time = ds['time']
        times = time.to_pandas()
        sfc_pressure = (ds['pressfc'][:]) / 100
        pressure = ds['ugrdprs']['lev']
        height_ft = (ds['hgtprs'][:, :]) * 3.28084
        height_sfc = (ds['hgtsfc'][:])  * 3.28084
        height_agl = height_ft - height_sfc
        pressure_grid, time_grid = np.meshgrid(pressure, time)
        ds['dwptprs'] = mpcalc.dewpoint_from_relative_humidity(ds['tmpprs'] * units('kelvin'), ds['rhprs'] * units('percent'))
        theta_e = mpcalc.equivalent_potential_temperature(ds['lev'] * units('hPa'), ds['tmpprs'] * units('kelvin'), ds['dwptprs']) 
        theta_e = theta_e.to_numpy()
        if model == 'NAM':
            theta_e = theta_e.reshape(29,21)
        if model == 'GFS0p25':
            theta_e = theta_e.reshape(29,13)
        if model == 'RAP':
            theta_e = theta_e.reshape(22,21)
        rh = ds['rhprs']
        lat = abs(round(float(ds['lat'].values), 1))
        lon = abs(round(float(ds['lon'].values), 1))
    
        if lon > 180:
            lon = 360 - lon
        else:
            lon = lon
    
        if lat >= 0:
            lat_symbol = '°N'
        else:
            lat_symbol = '°S'
    
        if lon <= 180:
            lon_symbol = '°W'
        else:
            lon_symbol = '°E'
        
        
        fig = plt.figure(figsize=(18, 7))
        fig.set_facecolor('aliceblue')
        gs = gridspec.GridSpec(10, 10)
    
        ax1 = fig.add_subplot(gs[0:10, 0:10])
        
        ax1.set_yscale('symlog')
        ax1.set_yticks(np.arange(1000, 50, -100))
        ax1.set_yticklabels(np.arange(1000, 50, -100))
        ax1.set_ylim(np.nanmax(sfc_pressure), 475)
        ax1.xaxis.set_major_formatter(md.DateFormatter('%d/%HZ'))
        ax1.set_xticks(time)

        low = np.nanmin(vv[:, :])
        high = np.nanmax(vv[:, :])

        if low < 0 and high >= 0:
            vv_range = abs(low) + high
        if low < 0 and high < 0 :
            vv_range = low - high
        if low >= 0 and high >= 0:
            vv_range = high - low

        step = round(vv_range/10, 1)

        if low < 0 and abs(low) > high and high >=0:
            upper_bound = round(abs(low),2)
            lower_bound = round(low,2)
        if low < 0 and high >= 0 and abs(low) <= high:
            lower_bound = round((high * -1),2)
            upper_bound = round(high,2)
        if low < 0 and high < 0:
            upper_bound = round(high,2)
            lower_bound = round(low,2)
        if low >= 0 and high >= 0:
            upper_bound = round(high,2)
            lower_bound = round(low,2)
        
        step_cs = round(vv_range/100, 2)

        step_c = 3
        low_bound = int(round(np.nanmin(theta_e), 0))
        up_bound = int(round(np.nanmax(theta_e), 0))
                            
        ax1.contourf(time_grid, pressure_grid, vv[:, :], levels=np.arange(lower_bound, (upper_bound + step_cs), step_cs), cmap=cmap, alpha=0.25, extend='both')
        c = ax1.contour(time_grid, pressure_grid, theta_e, levels = np.arange(low_bound, (up_bound + step_c), step_c), colors='black', zorder=2, linewidths=1, linestyles='-')
        ax1.clabel(c, levels = np.arange(low_bound, (up_bound + step_c), step_c), inline=True, fontsize=8, rightside_up=True)
        c1 = ax1.contour(time_grid, pressure_grid, rh, levels = np.arange(0, 110, 10), colors='green', zorder=2, linewidths=1, linestyles='--')
        ax1.clabel(c1, levels = np.arange(0, 110, 10), inline=True, fontsize=8, rightside_up=True)   
        c2 = ax1.contour(time_grid, pressure_grid, (ds['tmpprs'] - 273.15), levels=[-18,-12], colors='black', zorder=2, linewidths=1, linestyles='dotted')
        ax1.clabel(c2, levels=[-18,-12], inline=True, fontsize=8, rightside_up=True)
        ax1.barbs(time_grid, pressure_grid, u[:, :], v[:, :], clip_on=True, zorder=10, color='black', length=5, alpha=0.5)
        if station_id != 'Custom' or station_id != 'custom':
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: VERTICAL VELOCITY (SHADED) [Pa/s] & THETA-E [K] (SOLID CONTOURS) & RH [%] (DASHED CONTOURS) & WIND BARBS [MPH]\nSTATION: {station_id.upper()} - LAT: {str(round(lat,1))}{lat_symbol} | LON: {str(round(lon,1))}{lon_symbol}", fontsize=9, fontweight='bold', loc='left')
        else:
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: VERTICAL VELOCITY (SHADED) [Pa/s] & T THETA-E [K] (SOLID CONTOURS) & RH [%] (DASHED CONTOURS) & WIND BARBS [MPH]\nLAT: {str(round(lat,1))}{lat_symbol} | LON: {str(round(lon,1))}{lon_symbol}", fontsize=9, fontweight='bold', loc='left')
        try:
            plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[28].strftime('%a %d/%HZ')}", fontsize=8, fontweight='bold', loc='right')
        except Exception as e:
            plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[21].strftime('%a %d/%HZ')}", fontsize=8, fontweight='bold', loc='right')
        ax1.text(0.01, -0.08, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax1.text(0.8, -0.08, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
    
        wb = longitude - 6
        eb = longitude + 6
        nb = latitude + 3
        sb = latitude - 3
    
        ax2 = fig.add_subplot(gs[0:2, 8:10], projection=ccrs.PlateCarree())
        ax2.axis("off")
        ax2.set_extent([wb, eb, sb, nb], ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax2.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass    
    
        ax2.plot(longitude, latitude, marker='*', markersize=8, color='maroon', zorder=15)
        ax2.text(0.01, 0.01, "Reference System: "+reference_system, transform=ax2.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
    
        fig.savefig(f"{path}/{save_name}", bbox_inches='tight')
        plt.close(fig)
        print(f"Saved image of cross-section to {path_print}/{save_name}.")

    def plot_favorable_firewx_forecast(model, station_id, save_name, low_rh_threshold=15, high_wind_threshold=25, high_temperature_threshold=None, longitude=None, latitude=None, data=False, ds=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-'):
    
        r'''
            This function plots a time vs. pressure cross-section forecast for a given point. Paramters: Lower Atmosphere Favorable Fire Weather Forecast. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) NAM - North American Model
                   3) RAP - RAP for the CONUS
                   4) RAP 32 - 32km North American RAP
    
            2) station_id (String) - The 4-letter airport station identifier. 
                                     If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

            3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                                    Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 
    
            Optional Arguments:

            1) low_rh_threshold (Integer) - Default = 15. The threshold for the contour line that defines what extremely low relative humidity is.

            2) high_wind_threshold (Integer) - Default = 25. The threshold for the contour line that defines what high winds are.

            3) temperature_threshold (Integer) - Default = None. This is to be used if the user wishes to add temperature as a factor to what 
               defines favorable fire weather conditions. When set to None, only RH & Wind Speed/Gust are taken 
               into account. When set to an integer value, the temperature will also be taken into account. 

            4) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 
            
            5) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 
            
            6) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                and passing the data in or if the function needs to download the data. A value of False means the data
                is downloaded inside of the function while a value of True means the user is downloading the data outside
                of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                things, it is recommended to set this value to True and download the data outside of the function and pass
                it in so that the amount of data requests on the host servers can be minimized. 
    
    
            7) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 
    
            8) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                     wishes to use a reference system not on this list, please see items 17-23. 
                
                Reference Systems: 
                
                1) 'States & Counties'
                2) 'States Only'
                3) 'GACC Only'
                4) 'GACC & PSA'
                5) 'CWA Only'
                6) 'NWS CWAs & NWS Public Zones'
                7) 'NWS CWAs & NWS Fire Weather Zones'
                8) 'NWS CWAs & Counties'
                9) 'GACC & PSA & NWS Fire Weather Zones'
                10) 'GACC & PSA & NWS Public Zones'
                11) 'GACC & PSA & NWS CWA'
                12) 'GACC & PSA & Counties'
                13) 'GACC & Counties'
    
    
            9) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide state borders. 
    
            10) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide county borders. 
    
            11) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display GACC borders. 
    
            12) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display PSA borders.
    
            13) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display CWA borders.
    
            14) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.
    
            15) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.
    
            16) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 
    
            17) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 
    
            18) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 
    
            19) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 
    
            20) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 
    
            21) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 
    
            22) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 
    
            23) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 
    
            24) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                To change to a dashed line, users should set state_border_linestyle='--'. 
    
            25) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                To change to a dashed line, users should set county_border_linestyle='--'. 
    
            26) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                To change to a dashed line, users should set gacc_border_linestyle='--'. 
    
            27) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            28) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            29) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            30) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'.   
    
            Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones
    
            state_border_linewidth = state_border_linewidth
            county_border_linewidth = county_border_linewidth
            gacc_border_linewidth = gacc_border_linewidth
            cwa_border_linewidth = cwa_border_linewidth
            nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
            nws_public_zones_linewidth = nws_public_zones_linewidth
            psa_border_linewidth = psa_border_linewidth
    
        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
                state_border_linewidth=1 
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                state_border_linewidth=1 
                county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
                gacc_border_linewidth=1
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
                cwa_border_linewidth=1
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                cwa_border_linewidth=1
                nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                cwa_border_linewidth=1
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                cwa_border_linewidth=1
                county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_public_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                cwa_border_linewidth=0.25
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                county_border_linewidth=0.25 
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                county_border_linewidth=0.25 

        if data == False:
            if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
                ds = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
                
                longitude = ds['tmpprs']['lon'].values
                latitude = ds['tmpprs']['lat'].values
        
            else:
                if model == 'RAP 32' or model == 'rap 32':
                    ds = model_data.get_hourly_rap_data_point_forecast(model, station_id, longitude, latitude)
                else:
                    ds = model_data.get_nomads_opendap_data_point_forecast(model, station_id, longitude, latitude)
                
                
        if data == True:
    
            ds = ds.squeeze()
    
            if station_id == 'Custom' or station_id == 'custom':
                longitude = longitude 
                latitude = latitude
                
            else:
                longitude, latitude = station_coords(station_id)
    
            if model == 'GFS0p25' or model == 'GFS0p50' or model == 'NA NAM' or model == 'RAP 32' or model == 'rap 32':
                
                if longitude < 0:
                    longitude = 360 + longitude
                else:
                    longitude = longitude   
            
            ds = ds.sel(lon=longitude, lat=latitude, method='nearest')
        ds = ds.sel(time=ds['time'][0:29])

        if model == 'NAM' or model == 'RAP' or model == 'RAP 32':
            ds = ds.sel(lev=ds['lev'][0:21])
        if model == 'GFS0p25':
            ds = ds.sel(lev=ds['lev'][0:13])
    
        if station_id == 'Custom' or station_id == 'custom':
            longitude = longitude
            latitude = latitude
    
        else:
            longitude = ds['tmpprs']['lon'].values
            latitude = ds['tmpprs']['lat'].values
    
        if longitude > 180:
            longitude = (360 - longitude) * -1
        else:
            longitude = longitude
    
    
        path, path_print = file_functions.forecast_cross_sections_graphics_paths(model, 'Time Cross Section', 'Lower Atmosphere Favorable Fire Weather Forecast', reference_system)
    
        try:
            os.remove(f"{path}/{save_name}")
        except Exception as e:
            pass
    
        print(f"The old {save_name} file in {path_print} has been deleted.")
    
        title_lon = str(round(float(abs(longitude)), 1))
        title_lat = str(round(float(abs(latitude)), 1))
    
        cmap = colormaps.red_flag_warning_criteria_colormap()
    
        u = (ds['ugrdprs']) * 2.23694
        v = (ds['vgrdprs']) * 2.23694
        ws = np.hypot(u,v)
        
        time = ds['time']
        times = time.to_pandas()
        sfc_pressure = (ds['pressfc'][:]) / 100
        pressure = ds['ugrdprs']['lev']
        height_ft = (ds['hgtprs'][:, :]) * 3.28084
        height_sfc = (ds['hgtsfc'][:])  * 3.28084
        height_agl = height_ft - height_sfc
        pressure_grid, time_grid = np.meshgrid(pressure, time)
        temperature = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmpprs'])
        rh = ds['rhprs']
        lat = abs(round(float(ds['lat'].values), 1))
        lon = abs(round(float(ds['lon'].values), 1))
    
        if lon > 180:
            lon = 360 - lon
        else:
            lon = lon
    
        if lat >= 0:
            lat_symbol = '°N'
        else:
            lat_symbol = '°S'
    
        if lon <= 180:
            lon_symbol = '°W'
        else:
            lon_symbol = '°E'

        mask_top = sfc_pressure - 200

        if high_temperature_threshold == None:
            mask = (rh <= low_rh_threshold) & (ws >= high_wind_threshold) & (pressure >= mask_top)
        else:
            mask = (rh <= low_rh_threshold) & (ws >= high_wind_threshold) & (pressure >= mask_top) & (temperature >= high_temperature_threshold)
        
        
        fig = plt.figure(figsize=(18, 7))
        fig.set_facecolor('aliceblue')
        gs = gridspec.GridSpec(10, 10)
    
        ax1 = fig.add_subplot(gs[0:10, 0:10])
        
        ax1.set_yscale('symlog')
        ax1.set_yticks(np.arange(1000, 50, -100))
        ax1.set_yticklabels(np.arange(1000, 50, -100))
        ax1.set_ylim(np.nanmax(sfc_pressure), (np.nanmax(sfc_pressure) - 200))
        ax1.xaxis.set_major_formatter(md.DateFormatter('%d/%HZ'))
        ax1.set_xticks(time)

        try:
            ax1.pcolormesh(time_grid, pressure_grid, mask, cmap=cmap, alpha=0.25)
        except Exception as e:
            pass

        if high_temperature_threshold != None:


            c3 = ax1.contour(time_grid, pressure_grid, temperature, levels = np.arange(0, (int(round(np.nanmax(temperature),0)) + 5), 5), colors='darkred', zorder=2, linewidths=1, linestyles='dashdot')
            ax1.clabel(c3, levels = np.arange(0, (int(round(np.nanmax(temperature),0)) + 5), 5), inline=True, fontsize=8, rightside_up=True)      

        else:
            pass

        c1 = ax1.contour(time_grid, pressure_grid, rh, levels = np.arange(0, 110, 10), colors='darkgreen', zorder=2, linewidths=1, linestyles='--')
        ax1.clabel(c1, levels = np.arange(0, 110, 10), inline=True, fontsize=8, rightside_up=True)    
        ax1.barbs(time_grid, pressure_grid, u[:, :], v[:, :], clip_on=True, zorder=10, color='black', length=5, alpha=0.5)

        c2 = ax1.contour(time_grid, pressure_grid, ws, levels = np.arange(0, (np.nanmax(ws) + 5), 5), colors='darkorange', zorder=2, linewidths=1, linestyles='dotted')
        ax1.clabel(c2, levels = np.arange(0, (np.nanmax(ws) + 5), 5), inline=True, fontsize=8, rightside_up=True)            

        if high_temperature_threshold == None:
            if station_id != 'Custom' or station_id != 'custom':
                plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: FAVORABLE FIREWX FORECAST (SHADED RED) -> RH <= {low_rh_threshold} [%] & WIND SPEED >= {high_wind_threshold} [MPH]\nWIND SPEED (ORANGE CONTOURS) | RH (GREEN CONTOURS)\nSTATION: {station_id.upper()} - LAT: {str(round(lat,1))}{lat_symbol} | LON: {str(round(lon,1))}{lon_symbol}", fontsize=9, fontweight='bold', loc='left')
            else:
                plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: FAVORABLE FIREWX FORECAST (SHADED RED) -> RH <= {low_rh_threshold} [%] & WIND SPEED >= {high_wind_threshold} [MPH]\nWIND SPEED (ORANGE CONTOURS) | RH (GREEN CONTOURS)\nLAT: {str(round(lat,1))}{lat_symbol} | LON: {str(round(lon,1))}{lon_symbol}", fontsize=9, fontweight='bold', loc='left')

        else:
            if station_id != 'Custom' or station_id != 'custom':
                plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: FAVORABLE FIREWX FORECAST (SHADED RED) -> T >= {high_temperature_threshold} [°F] & RH <= {low_rh_threshold} [%] & WIND SPEED >= {high_wind_threshold} [MPH]\nTEMPERATURE (RED CONTOURS) | WIND SPEED (ORANGE CONTOURS) | RH (GREEN CONTOURS)\nSTATION: {station_id.upper()} - LAT: {str(round(lat,1))}{lat_symbol} | LON: {str(round(lon,1))}{lon_symbol}", fontsize=8, fontweight='bold', loc='left')
            else:
                plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: FAVORABLE FIREWX FORECAST (SHADED RED) -> T >= {high_temperature_threshold} [°F] & RH <= {low_rh_threshold} [%] & WIND SPEED >= {high_wind_threshold} [MPH]\nTEMPERATURE (RED CONTOURS) | WIND SPEED (ORANGE CONTOURS) | RH (GREEN CONTOURS)\nLAT: {str(round(lat,1))}{lat_symbol} | LON: {str(round(lon,1))}{lon_symbol}", fontsize=8, fontweight='bold', loc='left')            

        
        try:
            plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[28].strftime('%a %d/%HZ')}", fontsize=7, fontweight='bold', loc='right')
        except Exception as e:
            plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[21].strftime('%a %d/%HZ')}", fontsize=7, fontweight='bold', loc='right')
        ax1.text(0.01, -0.08, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
        ax1.text(0.8, -0.08, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
    
        wb = longitude - 6
        eb = longitude + 6
        nb = latitude + 3
        sb = latitude - 3
    
        ax2 = fig.add_subplot(gs[0:2, 8:10], projection=ccrs.PlateCarree())
        ax2.axis("off")
        ax2.set_extent([wb, eb, sb, nb], ccrs.PlateCarree())
        ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
        ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
        ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
        ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
        ax2.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
        if show_rivers == True:
            ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
        else:
            pass
    
        if show_gacc_borders == True:
            ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
        else:
            pass
        if show_psa_borders == True:
            ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
        else:
            pass
        if show_county_borders == True:
            ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
        else:
            pass
        if show_state_borders == True:
            ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
        else:
            pass
        if show_cwa_borders == True:
            ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
        else:
            pass
        if show_nws_firewx_zones == True:
            ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
        else:
            pass
        if show_nws_public_zones == True:
            ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
        else:
            pass    
    
        ax2.plot(longitude, latitude, marker='*', markersize=8, color='maroon', zorder=15)
        ax2.text(0.01, 0.01, "Reference System: "+reference_system, transform=ax2.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
    
        fig.savefig(f"{path}/{save_name}", bbox_inches='tight')
        plt.close(fig)
        print(f"Saved image of cross-section to {path_print}/{save_name}.")


class two_point_cross_sections:

    r'''
    This class hosts functions of forecast cross-sections between two points (lat/lon). 

    '''

    def plot_lower_atmosphere_wind(model, region, starting_point, ending_point, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', north_to_south=False):
    
        r'''
            This function plots forecast cross-sections between two points. Paramter: Lower Atmosphere Wind. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) NAM - North American Model
                   3) RAP - RAP for the CONUS
                   4) RAP 32 - 32km North American RAP
    
            2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                                 To look at any state use the 2-letter abbreviation for the state in either all capitals
                                 or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                                 CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                                 North America use either: NA, na, North America or north america. If the user wishes to use custom
                                 boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                                 the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                                 'oscc' for South Ops. 

            3) starting_point (Tuple) - (lat,lon) in decimal degrees. 

            4) ending_point (Tuple) - (lat,lon) in decimal degrees.
    
            Optional Arguments:
    
            
            1) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                and passing the data in or if the function needs to download the data. A value of False means the data
                is downloaded inside of the function while a value of True means the user is downloading the data outside
                of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                things, it is recommended to set this value to True and download the data outside of the function and pass
                it in so that the amount of data requests on the host servers can be minimized. 
    
    
            2) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

            3) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


            4) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


            5) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                         

            6) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
    
            7) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                     wishes to use a reference system not on this list, please see items 17-23. 
                
                Reference Systems: 
                
                1) 'States & Counties'
                2) 'States Only'
                3) 'GACC Only'
                4) 'GACC & PSA'
                5) 'CWA Only'
                6) 'NWS CWAs & NWS Public Zones'
                7) 'NWS CWAs & NWS Fire Weather Zones'
                8) 'NWS CWAs & Counties'
                9) 'GACC & PSA & NWS Fire Weather Zones'
                10) 'GACC & PSA & NWS Public Zones'
                11) 'GACC & PSA & NWS CWA'
                12) 'GACC & PSA & Counties'
                13) 'GACC & Counties'
    
    
            8) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide state borders. 
    
            9) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide county borders. 
    
            10) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display GACC borders. 
    
            11) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display PSA borders.
    
            12) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display CWA borders.
    
            13) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.
    
            14) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.
    
            15) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 
    
            16) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 
    
            17) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 
    
            18) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 
    
            19) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 
    
            20) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 
    
            21) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 
    
            22) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 
    
            23) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                To change to a dashed line, users should set state_border_linestyle='--'. 
    
            24) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                To change to a dashed line, users should set county_border_linestyle='--'. 
    
            25) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                To change to a dashed line, users should set gacc_border_linestyle='--'. 
    
            26) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            27) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            28) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            29) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'.   
    
            Returns: A set of graphic showing forecast cross-sections between two points saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Two Point Cross Section/{reference_system}/{parameters}/
        
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        if north_to_south == False:
            ref = 'lon'
        else:
            ref = 'lat'
    
        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones
    
            state_border_linewidth = state_border_linewidth
            county_border_linewidth = county_border_linewidth
            gacc_border_linewidth = gacc_border_linewidth
            cwa_border_linewidth = cwa_border_linewidth
            nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
            nws_public_zones_linewidth = nws_public_zones_linewidth
            psa_border_linewidth = psa_border_linewidth
    
        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
                state_border_linewidth=1 
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                state_border_linewidth=1 
                county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
                gacc_border_linewidth=1
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
                cwa_border_linewidth=1
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                cwa_border_linewidth=1
                nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                cwa_border_linewidth=1
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                cwa_border_linewidth=1
                county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_public_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                cwa_border_linewidth=0.25
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                county_border_linewidth=0.25 
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                county_border_linewidth=0.25 

        start_lon = starting_point[1]
        start_lat = starting_point[0]
        end_lon = ending_point[1]
        end_lat = ending_point[0]

        if region == 'Custom' or region == 'custom':

            if start_lon < end_lon:
                western_bound = start_lon
                eastern_bound = end_lon
            else:
                eastern_bound = start_lon
                western_bound = end_lon
    
            if start_lat < end_lat:
                southern_bound = start_lat
                northern_bound = end_lat
            else:
                northern_bound = start_lat
                southern_bound = end_lat
                                
            western_bound = western_bound - 1
            eastern_bound = eastern_bound + 1
            southern_bound = southern_bound - 1
            northern_bound = northern_bound + 1

        if data == False:
            if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                
        
            else:
                if model == 'RAP 32' or model == 'rap 32':
                    ds = model_data.get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                else:
                    ds = model_data.get_nomads_opendap_data(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                
                
        if data == True:

            ds = ds
    
        ds = ds.squeeze()
        if model == 'NAM' or model == 'RAP' or model == 'RAP 32':
            ds = ds.sel(lev=ds['lev'][0:21])
        if model == 'GFS0p25':
            ds = ds.sel(lev=ds['lev'][0:13])

        if model == 'GFS0p25' or model == 'RAP 32':
            ds['lon'] = (ds['lon'] - 360)
        else:
            pass

        sfc_pressure = ds['pressfc']/100
        u = (ds['ugrdprs']) * 2.23694
        v = (ds['vgrdprs']) * 2.23694
        gph_500 = (ds['hgtprs'][:, -1, :, :])/10
    
        ws = mpcalc.wind_speed(u * units('mph'), v * units('mph'))
        cross = cross_section(ws, starting_point, ending_point)
        u_cross = cross_section(u, starting_point, ending_point)
        v_cross = cross_section(v, starting_point, ending_point)
        height_cross = cross_section(sfc_pressure, starting_point, ending_point)
        ws_grid, pressure, index, lon, height = xr.broadcast(cross, cross['lev'], cross['index'], cross[ref], height_cross) 
    
        path, path_print = file_functions.forecast_cross_sections_graphics_paths(model, 'Two Point Cross Section', 'Lower Atmosphere Winds', reference_system, start_coords=starting_point, end_coords=ending_point)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
                
        print(f"Any old images (if any) in {path_print} have been deleted.")

        stop_loop = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()

        cmap = colormaps.cross_section_wind_speed()

        if stop_loop >= 100:
            step = 2
        else:
            step = 1

        stop = np.nanmax(ws[:,:])
        end = stop + 1
        nearest_10 = (round((stop/10),0) * 10) + 10
        nearest_5 = (round((stop/5),0) * 5) + 10

        min_lon = np.nanmin(cross['lon'])
        max_lon = np.nanmax(cross['lon'])
        min_lat = np.nanmin(cross['lat'])
        max_lat = np.nanmax(cross['lat'])

        wb = min_lon - 6
        eb = max_lon + 6
        nb = max_lat + 3
        sb = min_lat - 3

        start_lon = starting_point[1]
        start_lat = starting_point[0]
        end_lon = ending_point[1]
        end_lat = ending_point[0]
    
        if start_lat >= 0:
            start_lat_symbol = '°N'
        else:
            start_lat_symbol = '°S'
            
        if end_lat >= 0:
            end_lat_symbol = '°N'
        else:
            end_lat_symbol = '°S'
    
        if start_lon <= 180:
            start_lon_symbol = '°W'
        else:
            start_lon_symbol = '°E'

        if end_lon <= 180:
            end_lon_symbol = '°W'
        else:
            end_lon_symbol = '°E'

        if model == 'GFS0p25':
            decimate = 1
        else:
            decimate = 2
    
        for i in range(0, stop_loop, step):
    
            fname = f"Image_{i}.png"

            fig = plt.figure(figsize=(18, 7))
            gs = gridspec.GridSpec(10, 10)
            ax1 = fig.add_subplot(gs[0:10, 0:10])
            ax1.contourf(lon[i, :, :], pressure[i, :, :], ws_grid[i, :, :], cmap=cmap, levels=np.arange(0, end, 1), alpha=0.25)
            ax1.set_yscale('symlog')
            ax1.set_yticks(np.arange(1000, 50, -100))
            ax1.set_yticklabels(np.arange(1000, 50, -100))
            ax1.set_ylim(1000, 475)
            ax1.fill_between(lon[i, 0, :], height[i, 0, :], np.nanmax(sfc_pressure), color="black", zorder=10)
            ax1.barbs(lon[i, ::decimate, ::decimate], pressure[i, ::decimate, ::decimate], u_cross[i, ::decimate, ::decimate], v_cross[i, ::decimate, ::decimate], clip_on=True, zorder=10, color='black', length=5, alpha=0.5)
            c10 = ax1.contour(lon[i, :, :], pressure[i, :, :], ws_grid[i, :, :], levels=np.arange(0, nearest_10, 10), colors='black', zorder=2, linewidths=1)
            ax1.clabel(c10, levels=np.arange(0, nearest_10, 10), inline=True, fontsize=8, rightside_up=True)
            c5 = ax1.contour(lon[i, :, :], pressure[i, :, :], ws_grid[i, :, :], levels=np.arange(5, nearest_5, 10), colors='black', zorder=2, linewidths=1, linestyles='--')
            ax1.clabel(c5, levels=np.arange(5, nearest_5, 10), inline=True, fontsize=8, rightside_up=True)
            ax1.text(0.01, -0.08, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS | Map Reference System: "+reference_system, transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax1.text(0.8, -0.08, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)

            plt.title(f"{model.upper()} LOWER ATMOSPHERIC WIND [MPH]\nSTART: {str(abs(start_lat))}{start_lat_symbol}/{str(abs(start_lon))}{start_lon_symbol} END: {str(abs(end_lat))}{end_lat_symbol}/{str(abs(end_lon))}{end_lon_symbol}\nFORECAST VALID: {times.iloc[i].strftime('%a %d/%H UTC')} | INITIALIZATION: {times.iloc[0].strftime('%a %d/%H UTC')}", fontsize=10, fontweight='bold', loc='left')

            ax2 = fig.add_subplot(gs[0:2, 8:10], projection=ccrs.PlateCarree())
            ax2.axis("off")
            ax2.set_extent([wb, eb, sb, nb], ccrs.PlateCarree())
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax2.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass    

        
            ax2.plot(start_lon, start_lat, marker='*', markersize=8, color='k', zorder=15)
            ax2.plot(end_lon, end_lat, marker='*', markersize=8, color='k', zorder=15)
            ax2.plot(cross['lon'], cross['lat'], c='k', zorder=10)
            ax2.contourf(ds['lon'], ds['lat'], gph_500[i, :, :], levels=np.arange(480, 601, 1), cmap=colormaps.gph_colormap(), alpha=0.25, transform=datacrs, extend='both')
            ax2.text(0.01, 0.01, "Reference System: "+reference_system, transform=ax2.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
            ax2.set_title(f"500 MB GPH", fontweight='bold', fontsize=8)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            print(f"Saved image for forecast {times.iloc[i].strftime('%a %d/%H UTC')} to {path_print}.")
            tim.sleep(10)

            
    def plot_lower_atmosphere_vertical_velocity(model, region, starting_point, ending_point, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', north_to_south=False):
    
        r'''
            This function plots forecast cross-sections between two points. Paramter: Lower Atmosphere Vertical Velocity. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) NAM - North American Model
                   3) RAP - RAP for the CONUS
                   4) RAP 32 - 32km North American RAP
    
            2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                                 To look at any state use the 2-letter abbreviation for the state in either all capitals
                                 or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                                 CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                                 North America use either: NA, na, North America or north america. If the user wishes to use custom
                                 boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                                 the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                                 'oscc' for South Ops. 

            3) starting_point (Tuple) - (lat,lon) in decimal degrees. 

            4) ending_point (Tuple) - (lat,lon) in decimal degrees.
    
            Optional Arguments:
    
            
            1) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                and passing the data in or if the function needs to download the data. A value of False means the data
                is downloaded inside of the function while a value of True means the user is downloading the data outside
                of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                things, it is recommended to set this value to True and download the data outside of the function and pass
                it in so that the amount of data requests on the host servers can be minimized. 
    
    
            2) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

            3) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


            4) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


            5) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                         

            6) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
    
            7) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                     wishes to use a reference system not on this list, please see items 17-23. 
                
                Reference Systems: 
                
                1) 'States & Counties'
                2) 'States Only'
                3) 'GACC Only'
                4) 'GACC & PSA'
                5) 'CWA Only'
                6) 'NWS CWAs & NWS Public Zones'
                7) 'NWS CWAs & NWS Fire Weather Zones'
                8) 'NWS CWAs & Counties'
                9) 'GACC & PSA & NWS Fire Weather Zones'
                10) 'GACC & PSA & NWS Public Zones'
                11) 'GACC & PSA & NWS CWA'
                12) 'GACC & PSA & Counties'
                13) 'GACC & Counties'
    
    
            8) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide state borders. 
    
            9) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide county borders. 
    
            10) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display GACC borders. 
    
            11) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display PSA borders.
    
            12) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display CWA borders.
    
            13) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.
    
            14) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.
    
            15) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 
    
            16) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 
    
            17) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 
    
            18) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 
    
            19) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 
    
            20) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 
    
            21) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 
    
            22) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 
    
            23) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                To change to a dashed line, users should set state_border_linestyle='--'. 
    
            24) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                To change to a dashed line, users should set county_border_linestyle='--'. 
    
            25) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                To change to a dashed line, users should set gacc_border_linestyle='--'. 
    
            26) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            27) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            28) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            29) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'.   
    
            Returns: A set of graphic showing forecast cross-sections between two points saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Two Point Cross Section/{reference_system}/{parameters}/
        
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        if north_to_south == False:
            ref = 'lon'
        else:
            ref = 'lat'
    
        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones
    
            state_border_linewidth = state_border_linewidth
            county_border_linewidth = county_border_linewidth
            gacc_border_linewidth = gacc_border_linewidth
            cwa_border_linewidth = cwa_border_linewidth
            nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
            nws_public_zones_linewidth = nws_public_zones_linewidth
            psa_border_linewidth = psa_border_linewidth
    
        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
                state_border_linewidth=1 
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                state_border_linewidth=1 
                county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
                gacc_border_linewidth=1
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
                cwa_border_linewidth=1
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                cwa_border_linewidth=1
                nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                cwa_border_linewidth=1
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                cwa_border_linewidth=1
                county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_public_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                cwa_border_linewidth=0.25
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                county_border_linewidth=0.25 
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                county_border_linewidth=0.25 

        start_lon = starting_point[1]
        start_lat = starting_point[0]
        end_lon = ending_point[1]
        end_lat = ending_point[0]

        if region == 'Custom' or region == 'custom':

            if start_lon < end_lon:
                western_bound = start_lon
                eastern_bound = end_lon
            else:
                eastern_bound = start_lon
                western_bound = end_lon
    
            if start_lat < end_lat:
                southern_bound = start_lat
                northern_bound = end_lat
            else:
                northern_bound = start_lat
                southern_bound = end_lat
                                
            western_bound = western_bound - 1
            eastern_bound = eastern_bound + 1
            southern_bound = southern_bound - 1
            northern_bound = northern_bound + 1

        if data == False:
            if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                
        
            else:
                if model == 'RAP 32' or model == 'rap 32':
                    ds = model_data.get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                else:
                    ds = model_data.get_nomads_opendap_data(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                
                
        if data == True:

            ds = ds
    
        ds = ds.squeeze()
        if model == 'NAM' or model == 'RAP' or model == 'RAP 32':
            ds = ds.sel(lev=ds['lev'][0:21])
        if model == 'GFS0p25':
            ds = ds.sel(lev=ds['lev'][0:13])

        if model == 'GFS0p25' or model == 'RAP 32':
            ds['lon'] = (ds['lon'] - 360)
        else:
            pass

        sfc_pressure = ds['pressfc']/100
        gph_500 = (ds['hgtprs'][:, -1, :, :])/10
        vv = ds['vvelprs']
    
        cross = cross_section(vv, starting_point, ending_point)
        height_cross = cross_section(sfc_pressure, starting_point, ending_point)
        vv_grid, pressure, index, lon, height = xr.broadcast(cross, cross['lev'], cross['index'], cross[ref], height_cross) 
    
        path, path_print = file_functions.forecast_cross_sections_graphics_paths(model, 'Two Point Cross Section', 'Lower Atmosphere Vertical Velocity', reference_system, start_coords=starting_point, end_coords=ending_point)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
                
        print(f"Any old images (if any) in {path_print} have been deleted.")

        stop_loop = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()

        cmap = colormaps.vertical_velocity_colormap()

        if stop_loop >= 100:
            step = 2
        else:
            step = 1

        min_lon = np.nanmin(cross['lon'])
        max_lon = np.nanmax(cross['lon'])
        min_lat = np.nanmin(cross['lat'])
        max_lat = np.nanmax(cross['lat'])

        wb = min_lon - 6
        eb = max_lon + 6
        nb = max_lat + 3
        sb = min_lat - 3

        start_lon = starting_point[1]
        start_lat = starting_point[0]
        end_lon = ending_point[1]
        end_lat = ending_point[0]
    
        if start_lat >= 0:
            start_lat_symbol = '°N'
        else:
            start_lat_symbol = '°S'
            
        if end_lat >= 0:
            end_lat_symbol = '°N'
        else:
            end_lat_symbol = '°S'
    
        if start_lon <= 180:
            start_lon_symbol = '°W'
        else:
            start_lon_symbol = '°E'

        if end_lon <= 180:
            end_lon_symbol = '°W'
        else:
            end_lon_symbol = '°E'

        if model == 'GFS0p25':
            decimate = 1
        else:
            decimate = 2
    
        for i in range(0, stop_loop, step):

            low = np.nanmin(vv[i, :, :])
            high = np.nanmax(vv[i, :, :])
    
            if low < 0 and high >= 0:
                vv_range = abs(low) + high
            if low < 0 and high < 0 :
                vv_range = low - high
            if low >= 0 and high >= 0:
                vv_range = high - low
    
            step = round(vv_range/10, 1)
    
            if low < 0 and abs(low) > high and high >=0:
                upper_bound = round(abs(low),2)
                lower_bound = round(low,2)
            if low < 0 and high >= 0 and abs(low) <= high:
                lower_bound = round((high * -1),2)
                upper_bound = round(high,2)
            if low < 0 and high < 0:
                upper_bound = round(high,2)
                lower_bound = round(low,2)
            if low >= 0 and high >= 0:
                upper_bound = round(high,2)
                lower_bound = round(low,2)
            
            step_cs = round(vv_range/100, 2)
                            
    
            fname = f"Image_{i}.png"

            fig = plt.figure(figsize=(18, 7))
            gs = gridspec.GridSpec(10, 10)
            ax1 = fig.add_subplot(gs[0:10, 0:10])
            ax1.set_yscale('symlog')
            ax1.set_yticks(np.arange(1000, 50, -100))
            ax1.set_yticklabels(np.arange(1000, 50, -100))
            ax1.set_ylim(1000, 475)
            ax1.fill_between(lon[i, 0, :], height[i, 0, :], np.nanmax(sfc_pressure), color="black", zorder=10)
            ax1.contourf(lon[i, :, :], pressure[i, :, :], vv_grid[i, :, :], levels=np.arange(lower_bound, (upper_bound + step_cs), step_cs), cmap=cmap, alpha=0.25, extend='both')
            c = ax1.contour(lon[i, :, :], pressure[i, :, :], vv_grid[i, :, :], levels = np.arange(round(low, 1), round((high+step),1), round(step,1)), colors='black', zorder=2, linewidths=1, linestyles='--')
            ax1.clabel(c, levels = np.arange(round(low, 1), round((high+step),1), round(step,1)), inline=True, fontsize=8, rightside_up=True)
            ax1.text(0.01, -0.08, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS | Map Reference System: "+reference_system, transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax1.text(0.8, -0.08, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)

            plt.title(f"{model.upper()} LOWER ATMOSPHERIC VERTICAL VELOCITY [Pa/s]\nSTART: {str(abs(start_lat))}{start_lat_symbol}/{str(abs(start_lon))}{start_lon_symbol} END: {str(abs(end_lat))}{end_lat_symbol}/{str(abs(end_lon))}{end_lon_symbol}\nFORECAST VALID: {times.iloc[i].strftime('%a %d/%H UTC')} | INITIALIZATION: {times.iloc[0].strftime('%a %d/%H UTC')}", fontsize=10, fontweight='bold', loc='left')

            ax2 = fig.add_subplot(gs[0:2, 8:10], projection=ccrs.PlateCarree())
            ax2.axis("off")
            ax2.set_extent([wb, eb, sb, nb], ccrs.PlateCarree())
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax2.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass    

        
            ax2.plot(start_lon, start_lat, marker='*', markersize=8, color='k', zorder=15)
            ax2.plot(end_lon, end_lat, marker='*', markersize=8, color='k', zorder=15)
            ax2.plot(cross['lon'], cross['lat'], c='k', zorder=10)
            ax2.contourf(ds['lon'], ds['lat'], gph_500[i, :, :], levels=np.arange(480, 601, 1), cmap=colormaps.gph_colormap(), alpha=0.25, transform=datacrs, extend='both')
            ax2.text(0.01, 0.01, "Reference System: "+reference_system, transform=ax2.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
            ax2.set_title(f"500 MB GPH", fontweight='bold', fontsize=8)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            print(f"Saved image for forecast {times.iloc[i].strftime('%a %d/%H UTC')} to {path_print}.")
            tim.sleep(10)


    def plot_lower_atmosphere_temperature_rh_vertical_velocity_wind(model, region, starting_point, ending_point, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', north_to_south=False):
    
        r'''
            This function plots forecast cross-sections between two points. Paramter: Lower Atmosphere Temperature/RH/Vertical Velocity/Wind Barbs. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) NAM - North American Model
                   3) RAP - RAP for the CONUS
                   4) RAP 32 - 32km North American RAP
    
            2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                                 To look at any state use the 2-letter abbreviation for the state in either all capitals
                                 or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                                 CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                                 North America use either: NA, na, North America or north america. If the user wishes to use custom
                                 boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                                 the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                                 'oscc' for South Ops. 

            3) starting_point (Tuple) - (lat,lon) in decimal degrees. 

            4) ending_point (Tuple) - (lat,lon) in decimal degrees.
    
            Optional Arguments:
    
            
            1) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                and passing the data in or if the function needs to download the data. A value of False means the data
                is downloaded inside of the function while a value of True means the user is downloading the data outside
                of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                things, it is recommended to set this value to True and download the data outside of the function and pass
                it in so that the amount of data requests on the host servers can be minimized. 
    
    
            2) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

            3) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


            4) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


            5) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                         

            6) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
    
            7) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                     wishes to use a reference system not on this list, please see items 17-23. 
                
                Reference Systems: 
                
                1) 'States & Counties'
                2) 'States Only'
                3) 'GACC Only'
                4) 'GACC & PSA'
                5) 'CWA Only'
                6) 'NWS CWAs & NWS Public Zones'
                7) 'NWS CWAs & NWS Fire Weather Zones'
                8) 'NWS CWAs & Counties'
                9) 'GACC & PSA & NWS Fire Weather Zones'
                10) 'GACC & PSA & NWS Public Zones'
                11) 'GACC & PSA & NWS CWA'
                12) 'GACC & PSA & Counties'
                13) 'GACC & Counties'
    
    
            8) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide state borders. 
    
            9) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide county borders. 
    
            10) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display GACC borders. 
    
            11) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display PSA borders.
    
            12) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display CWA borders.
    
            13) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.
    
            14) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.
    
            15) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 
    
            16) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 
    
            17) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 
    
            18) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 
    
            19) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 
    
            20) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 
    
            21) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 
    
            22) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 
    
            23) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                To change to a dashed line, users should set state_border_linestyle='--'. 
    
            24) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                To change to a dashed line, users should set county_border_linestyle='--'. 
    
            25) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                To change to a dashed line, users should set gacc_border_linestyle='--'. 
    
            26) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            27) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            28) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            29) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'.   
    
            Returns: A set of graphic showing forecast cross-sections between two points saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Two Point Cross Section/{reference_system}/{parameters}/
        
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        if north_to_south == False:
            ref = 'lon'
        else:
            ref = 'lat'
    
        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones
    
            state_border_linewidth = state_border_linewidth
            county_border_linewidth = county_border_linewidth
            gacc_border_linewidth = gacc_border_linewidth
            cwa_border_linewidth = cwa_border_linewidth
            nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
            nws_public_zones_linewidth = nws_public_zones_linewidth
            psa_border_linewidth = psa_border_linewidth
    
        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
                state_border_linewidth=1 
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                state_border_linewidth=1 
                county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
                gacc_border_linewidth=1
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
                cwa_border_linewidth=1
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                cwa_border_linewidth=1
                nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                cwa_border_linewidth=1
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                cwa_border_linewidth=1
                county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_public_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                cwa_border_linewidth=0.25
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                county_border_linewidth=0.25 
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                county_border_linewidth=0.25 

        start_lon = starting_point[1]
        start_lat = starting_point[0]
        end_lon = ending_point[1]
        end_lat = ending_point[0]

        if region == 'Custom' or region == 'custom':

            if start_lon < end_lon:
                western_bound = start_lon
                eastern_bound = end_lon
            else:
                eastern_bound = start_lon
                western_bound = end_lon
    
            if start_lat < end_lat:
                southern_bound = start_lat
                northern_bound = end_lat
            else:
                northern_bound = start_lat
                southern_bound = end_lat
                                
            western_bound = western_bound - 1
            eastern_bound = eastern_bound + 1
            southern_bound = southern_bound - 1
            northern_bound = northern_bound + 1

        if data == False:
            if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                
        
            else:
                if model == 'RAP 32' or model == 'rap 32':
                    ds = model_data.get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                else:
                    ds = model_data.get_nomads_opendap_data(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                
                
        if data == True:

            ds = ds
    
        ds = ds.squeeze()
        if model == 'NAM' or model == 'RAP' or model == 'RAP 32':
            ds = ds.sel(lev=ds['lev'][0:21])
        if model == 'GFS0p25':
            ds = ds.sel(lev=ds['lev'][0:13])

        if model == 'GFS0p25' or model == 'RAP 32':
            ds['lon'] = (ds['lon'] - 360)
        else:
            pass

        sfc_pressure = ds['pressfc']/100
        gph_500 = (ds['hgtprs'][:, -1, :, :])/10
        vv = ds['vvelprs']
        u = (ds['ugrdprs']) * 2.23694
        v = (ds['vgrdprs']) * 2.23694
        temperature = ds['tmpprs'] - 273
        rh = ds['rhprs']
    
        cross = cross_section(vv, starting_point, ending_point)
        u_cross = cross_section(u, starting_point, ending_point)
        v_cross = cross_section(v, starting_point, ending_point)
        temp_cross = cross_section(temperature, starting_point, ending_point)
        rh_cross = cross_section(rh, starting_point, ending_point)
        height_cross = cross_section(sfc_pressure, starting_point, ending_point)
        vv_grid, pressure, index, lon, height = xr.broadcast(cross, cross['lev'], cross['index'], cross[ref], height_cross) 
    
        path, path_print = file_functions.forecast_cross_sections_graphics_paths(model, 'Two Point Cross Section', 'Lower Atmosphere Temperature & RH & Vertical Velocity & Wind Barbs', reference_system, start_coords=starting_point, end_coords=ending_point)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
                
        print(f"Any old images (if any) in {path_print} have been deleted.")

        stop_loop = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()

        cmap = colormaps.vertical_velocity_colormap()

        if stop_loop >= 100:
            step = 2
        else:
            step = 1

        min_lon = np.nanmin(cross['lon'])
        max_lon = np.nanmax(cross['lon'])
        min_lat = np.nanmin(cross['lat'])
        max_lat = np.nanmax(cross['lat'])
        
        wb = min_lon - 6
        eb = max_lon + 6
        nb = max_lat + 3
        sb = min_lat - 3   

        start_lon = starting_point[1]
        start_lat = starting_point[0]
        end_lon = ending_point[1]
        end_lat = ending_point[0]
    
        if start_lat >= 0:
            start_lat_symbol = '°N'
        else:
            start_lat_symbol = '°S'
            
        if end_lat >= 0:
            end_lat_symbol = '°N'
        else:
            end_lat_symbol = '°S'
    
        if start_lon <= 180:
            start_lon_symbol = '°W'
        else:
            start_lon_symbol = '°E'

        if end_lon <= 180:
            end_lon_symbol = '°W'
        else:
            end_lon_symbol = '°E'

        if model == 'GFS0p25':
            decimate = 1
        else:
            decimate = 2
    
        for i in range(0, stop_loop, step):

            low = np.nanmin(vv[i, :, :])
            high = np.nanmax(vv[i, :, :])
    
            if low < 0 and high >= 0:
                vv_range = abs(low) + high
            if low < 0 and high < 0 :
                vv_range = low - high
            if low >= 0 and high >= 0:
                vv_range = high - low
    
            step = round(vv_range/10, 1)
    
            if low < 0 and abs(low) > high and high >=0:
                upper_bound = round(abs(low),2)
                lower_bound = round(low,2)
            if low < 0 and high >= 0 and abs(low) <= high:
                lower_bound = round((high * -1),2)
                upper_bound = round(high,2)
            if low < 0 and high < 0:
                upper_bound = round(high,2)
                lower_bound = round(low,2)
            if low >= 0 and high >= 0:
                upper_bound = round(high,2)
                lower_bound = round(low,2)
            
            step_cs = round(vv_range/100, 2)

            step_c = 3
            start_c = round(np.nanmin(temperature[i, :, :]),0)
            stop_c = (round(np.nanmax(temperature[i, :, :]),0) + step_c)
                            
    
            fname = f"Image_{i}.png"

            fig = plt.figure(figsize=(18, 7))
            gs = gridspec.GridSpec(10, 10)
            ax1 = fig.add_subplot(gs[0:10, 0:10])
            ax1.set_yscale('symlog')
            ax1.set_yticks(np.arange(1000, 50, -100))
            ax1.set_yticklabels(np.arange(1000, 50, -100))
            ax1.set_ylim(1000, 475)
            ax1.fill_between(lon[i, 0, :], height[i, 0, :], np.nanmax(sfc_pressure), color="black", zorder=10)
            ax1.contourf(lon[i, :, :], pressure[i, :, :], vv_grid[i, :, :], levels=np.arange(lower_bound, (upper_bound + step_cs), step_cs), cmap=cmap, alpha=0.25, extend='both')

            c = ax1.contour(lon[i, :, :], pressure[i, :, :], temp_cross[i, :, :], levels = np.arange(start_c, (stop_c + step_c), step_c), colors='black', zorder=2, linewidths=1, linestyles='-')
            ax1.clabel(c, levels = np.arange(start_c, (stop_c + step_c), step_c), inline=True, fontsize=8, rightside_up=True)
            c1 = ax1.contour(lon[i, :, :], pressure[i, :, :], rh_cross[i, :, :], levels = np.arange(0, 110, 10), colors='green', zorder=2, linewidths=1, linestyles='--')
            ax1.clabel(c1, levels = np.arange(0, 110, 10), inline=True, fontsize=8, rightside_up=True)  
            c2 = ax1.contour(lon[i, :, :], pressure[i, :, :], temp_cross[i, :, :], levels=[-18,-12], colors='black', zorder=2, linewidths=1, linestyles='dotted')
            ax1.clabel(c2, levels=[-18,-12], inline=True, fontsize=8, rightside_up=True)
 
            ax1.barbs(lon[i, ::decimate, ::decimate], pressure[i, ::decimate, ::decimate], u_cross[i, ::decimate, ::decimate], v_cross[i, ::decimate, ::decimate], clip_on=True, zorder=10, color='black', length=5, alpha=0.5)
            ax1.text(0.01, -0.08, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS | Map Reference System: "+reference_system, transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax1.text(0.8, -0.08, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)

            plt.title(f"{model.upper()} LOWER ATMOSPHERIC VERTICAL VELOCITY (SHADED) [Pa/s] & T [°C] (SOLID CONTOURS) & RH [%] (DASHED CONTOURS) & WIND BARBS [MPH]\nSTART: {str(abs(start_lat))}{start_lat_symbol}/{str(abs(start_lon))}{start_lon_symbol} END: {str(abs(end_lat))}{end_lat_symbol}/{str(abs(end_lon))}{end_lon_symbol}\nFORECAST VALID: {times.iloc[i].strftime('%a %d/%H UTC')} | INITIALIZATION: {times.iloc[0].strftime('%a %d/%H UTC')}", fontsize=10, fontweight='bold', loc='left')

            ax2 = fig.add_subplot(gs[0:2, 8:10], projection=ccrs.PlateCarree())
            ax2.axis("off")
            ax2.set_extent([wb, eb, sb, nb], ccrs.PlateCarree())
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax2.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass    

        
            ax2.plot(start_lon, start_lat, marker='*', markersize=8, color='k', zorder=15)
            ax2.plot(end_lon, end_lat, marker='*', markersize=8, color='k', zorder=15)
            ax2.plot(cross['lon'], cross['lat'], c='k', zorder=10)
            ax2.contourf(ds['lon'], ds['lat'], gph_500[i, :, :], levels=np.arange(480, 601, 1), cmap=colormaps.gph_colormap(), alpha=0.25, transform=datacrs, extend='both')
            ax2.set_title(f"500 MB GPH", fontweight='bold', fontsize=8)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            print(f"Saved image for forecast {times.iloc[i].strftime('%a %d/%H UTC')} to {path_print}.")
            tim.sleep(10)


    def plot_lower_atmosphere_temperature_and_wind(model, region, starting_point, ending_point, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', north_to_south=False):
    
        r'''
            This function plots forecast cross-sections between two points. Paramter: Lower Atmosphere Temperature & Wind Barbs. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) NAM - North American Model
                   3) RAP - RAP for the CONUS
                   4) RAP 32 - 32km North American RAP
    
            2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                                 To look at any state use the 2-letter abbreviation for the state in either all capitals
                                 or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                                 CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                                 North America use either: NA, na, North America or north america. If the user wishes to use custom
                                 boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                                 the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                                 'oscc' for South Ops. 

            3) starting_point (Tuple) - (lat,lon) in decimal degrees. 

            4) ending_point (Tuple) - (lat,lon) in decimal degrees.
    
            Optional Arguments:
    
            
            1) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                and passing the data in or if the function needs to download the data. A value of False means the data
                is downloaded inside of the function while a value of True means the user is downloading the data outside
                of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                things, it is recommended to set this value to True and download the data outside of the function and pass
                it in so that the amount of data requests on the host servers can be minimized. 
    
    
            2) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

            3) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


            4) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


            5) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                         

            6) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
    
            7) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                     wishes to use a reference system not on this list, please see items 17-23. 
                
                Reference Systems: 
                
                1) 'States & Counties'
                2) 'States Only'
                3) 'GACC Only'
                4) 'GACC & PSA'
                5) 'CWA Only'
                6) 'NWS CWAs & NWS Public Zones'
                7) 'NWS CWAs & NWS Fire Weather Zones'
                8) 'NWS CWAs & Counties'
                9) 'GACC & PSA & NWS Fire Weather Zones'
                10) 'GACC & PSA & NWS Public Zones'
                11) 'GACC & PSA & NWS CWA'
                12) 'GACC & PSA & Counties'
                13) 'GACC & Counties'
    
    
            8) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide state borders. 
    
            9) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide county borders. 
    
            10) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display GACC borders. 
    
            11) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display PSA borders.
    
            12) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display CWA borders.
    
            13) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.
    
            14) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.
    
            15) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 
    
            16) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 
    
            17) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 
    
            18) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 
    
            19) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 
    
            20) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 
    
            21) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 
    
            22) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 
    
            23) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                To change to a dashed line, users should set state_border_linestyle='--'. 
    
            24) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                To change to a dashed line, users should set county_border_linestyle='--'. 
    
            25) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                To change to a dashed line, users should set gacc_border_linestyle='--'. 
    
            26) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            27) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            28) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            29) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'.   
    
            Returns: A set of graphic showing forecast cross-sections between two points saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Two Point Cross Section/{reference_system}/{parameters}/
        
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        if north_to_south == False:
            ref = 'lon'
        else:
            ref = 'lat'
    
        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones
    
            state_border_linewidth = state_border_linewidth
            county_border_linewidth = county_border_linewidth
            gacc_border_linewidth = gacc_border_linewidth
            cwa_border_linewidth = cwa_border_linewidth
            nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
            nws_public_zones_linewidth = nws_public_zones_linewidth
            psa_border_linewidth = psa_border_linewidth
    
        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
                state_border_linewidth=1 
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                state_border_linewidth=1 
                county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
                gacc_border_linewidth=1
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
                cwa_border_linewidth=1
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                cwa_border_linewidth=1
                nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                cwa_border_linewidth=1
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                cwa_border_linewidth=1
                county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_public_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                cwa_border_linewidth=0.25
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                county_border_linewidth=0.25 
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                county_border_linewidth=0.25 

        start_lon = starting_point[1]
        start_lat = starting_point[0]
        end_lon = ending_point[1]
        end_lat = ending_point[0]

        if region == 'Custom' or region == 'custom':

            if start_lon < end_lon:
                western_bound = start_lon
                eastern_bound = end_lon
            else:
                eastern_bound = start_lon
                western_bound = end_lon
    
            if start_lat < end_lat:
                southern_bound = start_lat
                northern_bound = end_lat
            else:
                northern_bound = start_lat
                southern_bound = end_lat
                                
            western_bound = western_bound - 1
            eastern_bound = eastern_bound + 1
            southern_bound = southern_bound - 1
            northern_bound = northern_bound + 1

        if data == False:
            if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                
        
            else:
                if model == 'RAP 32' or model == 'rap 32':
                    ds = model_data.get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                else:
                    ds = model_data.get_nomads_opendap_data(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                
                
        if data == True:

            ds = ds
    
        ds = ds.squeeze()
        if model == 'NAM' or model == 'RAP' or model == 'RAP 32':
            ds = ds.sel(lev=ds['lev'][0:21])
        if model == 'GFS0p25':
            ds = ds.sel(lev=ds['lev'][0:13])

        if model == 'GFS0p25' or model == 'RAP 32':
            ds['lon'] = (ds['lon'] - 360)
        else:
            pass

        sfc_pressure = ds['pressfc']/100
        gph_500 = (ds['hgtprs'][:, -1, :, :])/10
        u = (ds['ugrdprs']) * 2.23694
        v = (ds['vgrdprs']) * 2.23694
        temperature = ds['tmpprs'] - 273
    
        cross = cross_section(temperature, starting_point, ending_point)
        u_cross = cross_section(u, starting_point, ending_point)
        v_cross = cross_section(v, starting_point, ending_point)
        height_cross = cross_section(sfc_pressure, starting_point, ending_point)
        temp_grid, pressure, index, lon, height = xr.broadcast(cross, cross['lev'], cross['index'], cross[ref], height_cross) 
    
        path, path_print = file_functions.forecast_cross_sections_graphics_paths(model, 'Two Point Cross Section', 'Lower Atmosphere Temperature & Wind Barbs', reference_system, start_coords=starting_point, end_coords=ending_point)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
                
        print(f"Any old images (if any) in {path_print} have been deleted.")

        stop_loop = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()

        cmap = colormaps.temperature_colormap()

        if stop_loop >= 100:
            step = 2
        else:
            step = 1

        min_lon = np.nanmin(cross['lon'])
        max_lon = np.nanmax(cross['lon'])
        min_lat = np.nanmin(cross['lat'])
        max_lat = np.nanmax(cross['lat'])

        wb = min_lon - 6
        eb = max_lon + 6
        nb = max_lat + 3
        sb = min_lat - 3

        start_lon = starting_point[1]
        start_lat = starting_point[0]
        end_lon = ending_point[1]
        end_lat = ending_point[0]
    
        if start_lat >= 0:
            start_lat_symbol = '°N'
        else:
            start_lat_symbol = '°S'
            
        if end_lat >= 0:
            end_lat_symbol = '°N'
        else:
            end_lat_symbol = '°S'
    
        if start_lon <= 180:
            start_lon_symbol = '°W'
        else:
            start_lon_symbol = '°E'

        if end_lon <= 180:
            end_lon_symbol = '°W'
        else:
            end_lon_symbol = '°E'

        if model == 'GFS0p25':
            decimate = 1
        else:
            decimate = 2
    
        for i in range(0, stop_loop, step):

            step_c = 1
            start_c = round(np.nanmin(temperature[i, :, :]),0)
            stop_c = (round(np.nanmax(temperature[i, :, :]),0) + step_c)
                            
    
            fname = f"Image_{i}.png"

            fig = plt.figure(figsize=(18, 7))
            gs = gridspec.GridSpec(10, 10)
            ax1 = fig.add_subplot(gs[0:10, 0:10])
            ax1.set_yscale('symlog')
            ax1.set_yticks(np.arange(1000, 50, -100))
            ax1.set_yticklabels(np.arange(1000, 50, -100))
            ax1.set_ylim(1000, 475)
            ax1.fill_between(lon[i, 0, :], height[i, 0, :], np.nanmax(sfc_pressure), color="black", zorder=10)
            ax1.contourf(lon[i, :, :], pressure[i, :, :], temp_grid[i, :, :], levels=np.arange(start_c, (stop_c + step_c), step_c), cmap=cmap, alpha=0.25, extend='both')
            c = ax1.contour(lon[i, :, :], pressure[i, :, :], temp_grid[i, :, :], levels = np.arange(start_c, (stop_c + 3), 3), colors='black', zorder=2, linewidths=1, linestyles='-')
            ax1.clabel(c, levels = np.arange(start_c, (stop_c + 3), 3), inline=True, fontsize=8, rightside_up=True)
 
            ax1.barbs(lon[i, ::decimate, ::decimate], pressure[i, ::decimate, ::decimate], u_cross[i, ::decimate, ::decimate], v_cross[i, ::decimate, ::decimate], clip_on=True, zorder=10, color='black', length=5, alpha=0.5)
            ax1.text(0.01, -0.08, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS | Map Reference System: "+reference_system, transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax1.text(0.8, -0.08, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)

            plt.title(f"{model.upper()} LOWER ATMOSPHERIC TEMPERATURE [°C] & WIND BARBS [MPH]\nSTART: {str(abs(start_lat))}{start_lat_symbol}/{str(abs(start_lon))}{start_lon_symbol} END: {str(abs(end_lat))}{end_lat_symbol}/{str(abs(end_lon))}{end_lon_symbol}\nFORECAST VALID: {times.iloc[i].strftime('%a %d/%H UTC')} | INITIALIZATION: {times.iloc[0].strftime('%a %d/%H UTC')}", fontsize=10, fontweight='bold', loc='left')

            ax2 = fig.add_subplot(gs[0:2, 8:10], projection=ccrs.PlateCarree())
            ax2.axis("off")
            ax2.set_extent([wb, eb, sb, nb], ccrs.PlateCarree())
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax2.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass    

        
            ax2.plot(start_lon, start_lat, marker='*', markersize=8, color='k', zorder=15)
            ax2.plot(end_lon, end_lat, marker='*', markersize=8, color='k', zorder=15)
            ax2.plot(cross['lon'], cross['lat'], c='k', zorder=10)
            ax2.contourf(ds['lon'], ds['lat'], gph_500[i, :, :], levels=np.arange(480, 601, 1), cmap=colormaps.gph_colormap(), alpha=0.25, transform=datacrs, extend='both')
            ax2.text(0.01, 0.01, "Reference System: "+reference_system, transform=ax2.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
            ax2.set_title(f"500 MB GPH", fontweight='bold', fontsize=8)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            print(f"Saved image for forecast {times.iloc[i].strftime('%a %d/%H UTC')} to {path_print}.")
            tim.sleep(10)


    def plot_lower_atmosphere_relative_humidity_and_wind(model, region, starting_point, ending_point, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', north_to_south=False):
    
        r'''
            This function plots forecast cross-sections between two points. Paramter: Lower Atmosphere RH & Wind Barbs. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) NAM - North American Model
                   3) RAP - RAP for the CONUS
                   4) RAP 32 - 32km North American RAP
    
            2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                                 To look at any state use the 2-letter abbreviation for the state in either all capitals
                                 or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                                 CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                                 North America use either: NA, na, North America or north america. If the user wishes to use custom
                                 boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                                 the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                                 'oscc' for South Ops. 

            3) starting_point (Tuple) - (lat,lon) in decimal degrees. 

            4) ending_point (Tuple) - (lat,lon) in decimal degrees.
    
            Optional Arguments:
    
            
            1) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                and passing the data in or if the function needs to download the data. A value of False means the data
                is downloaded inside of the function while a value of True means the user is downloading the data outside
                of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                things, it is recommended to set this value to True and download the data outside of the function and pass
                it in so that the amount of data requests on the host servers can be minimized. 
    
    
            2) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

            3) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


            4) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


            5) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                         

            6) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
    
            7) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                     wishes to use a reference system not on this list, please see items 17-23. 
                
                Reference Systems: 
                
                1) 'States & Counties'
                2) 'States Only'
                3) 'GACC Only'
                4) 'GACC & PSA'
                5) 'CWA Only'
                6) 'NWS CWAs & NWS Public Zones'
                7) 'NWS CWAs & NWS Fire Weather Zones'
                8) 'NWS CWAs & Counties'
                9) 'GACC & PSA & NWS Fire Weather Zones'
                10) 'GACC & PSA & NWS Public Zones'
                11) 'GACC & PSA & NWS CWA'
                12) 'GACC & PSA & Counties'
                13) 'GACC & Counties'
    
    
            8) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide state borders. 
    
            9) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide county borders. 
    
            10) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display GACC borders. 
    
            11) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display PSA borders.
    
            12) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display CWA borders.
    
            13) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.
    
            14) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.
    
            15) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 
    
            16) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 
    
            17) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 
    
            18) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 
    
            19) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 
    
            20) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 
    
            21) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 
    
            22) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 
    
            23) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                To change to a dashed line, users should set state_border_linestyle='--'. 
    
            24) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                To change to a dashed line, users should set county_border_linestyle='--'. 
    
            25) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                To change to a dashed line, users should set gacc_border_linestyle='--'. 
    
            26) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            27) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            28) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            29) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'.   
    
            Returns: A set of graphic showing forecast cross-sections between two points saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Two Point Cross Section/{reference_system}/{parameters}/
        
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        if north_to_south == False:
            ref = 'lon'
        else:
            ref = 'lat'
            
        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones
    
            state_border_linewidth = state_border_linewidth
            county_border_linewidth = county_border_linewidth
            gacc_border_linewidth = gacc_border_linewidth
            cwa_border_linewidth = cwa_border_linewidth
            nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
            nws_public_zones_linewidth = nws_public_zones_linewidth
            psa_border_linewidth = psa_border_linewidth
    
        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
                state_border_linewidth=1 
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                state_border_linewidth=1 
                county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
                gacc_border_linewidth=1
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
                cwa_border_linewidth=1
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                cwa_border_linewidth=1
                nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                cwa_border_linewidth=1
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                cwa_border_linewidth=1
                county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_public_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                cwa_border_linewidth=0.25
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                county_border_linewidth=0.25 
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                county_border_linewidth=0.25 

        start_lon = starting_point[1]
        start_lat = starting_point[0]
        end_lon = ending_point[1]
        end_lat = ending_point[0]

        if region == 'Custom' or region == 'custom':

            if start_lon < end_lon:
                western_bound = start_lon
                eastern_bound = end_lon
            else:
                eastern_bound = start_lon
                western_bound = end_lon
    
            if start_lat < end_lat:
                southern_bound = start_lat
                northern_bound = end_lat
            else:
                northern_bound = start_lat
                southern_bound = end_lat
                                
            western_bound = western_bound - 1
            eastern_bound = eastern_bound + 1
            southern_bound = southern_bound - 1
            northern_bound = northern_bound + 1

        if data == False:
            if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                
        
            else:
                if model == 'RAP 32' or model == 'rap 32':
                    ds = model_data.get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                else:
                    ds = model_data.get_nomads_opendap_data(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                
                
        if data == True:

            ds = ds
    
        ds = ds.squeeze()
        if model == 'NAM' or model == 'RAP' or model == 'RAP 32':
            ds = ds.sel(lev=ds['lev'][0:21])
        if model == 'GFS0p25':
            ds = ds.sel(lev=ds['lev'][0:13])

        if model == 'GFS0p25' or model == 'RAP 32':
            ds['lon'] = (ds['lon'] - 360)
        else:
            pass

        sfc_pressure = ds['pressfc']/100
        gph_500 = (ds['hgtprs'][:, -1, :, :])/10
        u = (ds['ugrdprs']) * 2.23694
        v = (ds['vgrdprs']) * 2.23694
        rh = ds['rhprs']
    
        cross = cross_section(rh, starting_point, ending_point)
        u_cross = cross_section(u, starting_point, ending_point)
        v_cross = cross_section(v, starting_point, ending_point)
        height_cross = cross_section(sfc_pressure, starting_point, ending_point)
        rh_grid, pressure, index, lon, height = xr.broadcast(cross, cross['lev'], cross['index'], cross[ref], height_cross) 
    
        path, path_print = file_functions.forecast_cross_sections_graphics_paths(model, 'Two Point Cross Section', 'Lower Atmosphere RH & Wind Barbs', reference_system, start_coords=starting_point, end_coords=ending_point)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
                
        print(f"Any old images (if any) in {path_print} have been deleted.")

        stop_loop = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()

        cmap = colormaps.relative_humidity_colormap()

        if stop_loop >= 100:
            step = 2
        else:
            step = 1

        min_lon = np.nanmin(cross['lon'])
        max_lon = np.nanmax(cross['lon'])
        min_lat = np.nanmin(cross['lat'])
        max_lat = np.nanmax(cross['lat'])

        wb = min_lon - 6
        eb = max_lon + 6
        nb = max_lat + 3
        sb = min_lat - 3

        start_lon = starting_point[1]
        start_lat = starting_point[0]
        end_lon = ending_point[1]
        end_lat = ending_point[0]
    
        if start_lat >= 0:
            start_lat_symbol = '°N'
        else:
            start_lat_symbol = '°S'
            
        if end_lat >= 0:
            end_lat_symbol = '°N'
        else:
            end_lat_symbol = '°S'
    
        if start_lon <= 180:
            start_lon_symbol = '°W'
        else:
            start_lon_symbol = '°E'

        if end_lon <= 180:
            end_lon_symbol = '°W'
        else:
            end_lon_symbol = '°E'

        if model == 'GFS0p25':
            decimate = 1
        else:
            decimate = 2
    
        for i in range(0, stop_loop, step):
                            
    
            fname = f"Image_{i}.png"

            fig = plt.figure(figsize=(18, 7))
            gs = gridspec.GridSpec(10, 10)
            ax1 = fig.add_subplot(gs[0:10, 0:10])
            ax1.set_yscale('symlog')
            ax1.set_yticks(np.arange(1000, 50, -100))
            ax1.set_yticklabels(np.arange(1000, 50, -100))
            ax1.set_ylim(1000, 475)
            ax1.fill_between(lon[i, 0, :], height[i, 0, :], np.nanmax(sfc_pressure), color="black", zorder=10)
            ax1.contourf(lon[i, :, :], pressure[i, :, :], rh_grid[i, :, :], levels=np.arange(0, 102, 1), cmap=cmap, alpha=0.25, extend='both')
            c = ax1.contour(lon[i, :, :], pressure[i, :, :], rh_grid[i, :, :], levels = np.arange(0, 110, 10), colors='blue', zorder=2, linewidths=1, linestyles='--')
            ax1.clabel(c, levels = np.arange(0, 110, 10), inline=True, fontsize=8, rightside_up=True)
 
            ax1.barbs(lon[i, ::decimate, ::decimate], pressure[i, ::decimate, ::decimate], u_cross[i, ::decimate, ::decimate], v_cross[i, ::decimate, ::decimate], clip_on=True, zorder=10, color='black', length=5, alpha=0.5)
            ax1.text(0.01, -0.08, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS | Map Reference System: "+reference_system, transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax1.text(0.8, -0.08, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)

            plt.title(f"{model.upper()} LOWER ATMOSPHERIC RELATIVE HUMIDITY [%] & WIND BARBS [MPH]\nSTART: {str(abs(start_lat))}{start_lat_symbol}/{str(abs(start_lon))}{start_lon_symbol} END: {str(abs(end_lat))}{end_lat_symbol}/{str(abs(end_lon))}{end_lon_symbol}\nFORECAST VALID: {times.iloc[i].strftime('%a %d/%H UTC')} | INITIALIZATION: {times.iloc[0].strftime('%a %d/%H UTC')}", fontsize=10, fontweight='bold', loc='left')

            ax2 = fig.add_subplot(gs[0:2, 8:10], projection=ccrs.PlateCarree())
            ax2.axis("off")
            ax2.set_extent([wb, eb, sb, nb], ccrs.PlateCarree())
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax2.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass    

        
            ax2.plot(start_lon, start_lat, marker='*', markersize=8, color='k', zorder=15)
            ax2.plot(end_lon, end_lat, marker='*', markersize=8, color='k', zorder=15)
            ax2.plot(cross['lon'], cross['lat'], c='k', zorder=10)
            ax2.contourf(ds['lon'], ds['lat'], gph_500[i, :, :], levels=np.arange(480, 601, 1), cmap=colormaps.gph_colormap(), alpha=0.25, transform=datacrs, extend='both')
            ax2.text(0.01, 0.01, "Reference System: "+reference_system, transform=ax2.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
            ax2.set_title(f"500 MB GPH", fontweight='bold', fontsize=8)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            print(f"Saved image for forecast {times.iloc[i].strftime('%a %d/%H UTC')} to {path_print}.")
            tim.sleep(10)

    def plot_lower_atmosphere_theta_e_and_wind(model, region, starting_point, ending_point, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', north_to_south=False):
    
        r'''
            This function plots forecast cross-sections between two points. Paramter: Lower Atmosphere Theta-E & Wind Barbs. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) NAM - North American Model
                   3) RAP - RAP for the CONUS
                   4) RAP 32 - 32km North American RAP
    
            2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                                 To look at any state use the 2-letter abbreviation for the state in either all capitals
                                 or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                                 CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                                 North America use either: NA, na, North America or north america. If the user wishes to use custom
                                 boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                                 the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                                 'oscc' for South Ops. 

            3) starting_point (Tuple) - (lat,lon) in decimal degrees. 

            4) ending_point (Tuple) - (lat,lon) in decimal degrees.
    
            Optional Arguments:
    
            
            1) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                and passing the data in or if the function needs to download the data. A value of False means the data
                is downloaded inside of the function while a value of True means the user is downloading the data outside
                of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                things, it is recommended to set this value to True and download the data outside of the function and pass
                it in so that the amount of data requests on the host servers can be minimized. 
    
    
            2) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

            3) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


            4) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


            5) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                         

            6) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
    
            7) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                     wishes to use a reference system not on this list, please see items 17-23. 
                
                Reference Systems: 
                
                1) 'States & Counties'
                2) 'States Only'
                3) 'GACC Only'
                4) 'GACC & PSA'
                5) 'CWA Only'
                6) 'NWS CWAs & NWS Public Zones'
                7) 'NWS CWAs & NWS Fire Weather Zones'
                8) 'NWS CWAs & Counties'
                9) 'GACC & PSA & NWS Fire Weather Zones'
                10) 'GACC & PSA & NWS Public Zones'
                11) 'GACC & PSA & NWS CWA'
                12) 'GACC & PSA & Counties'
                13) 'GACC & Counties'
    
    
            8) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide state borders. 
    
            9) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide county borders. 
    
            10) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display GACC borders. 
    
            11) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display PSA borders.
    
            12) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display CWA borders.
    
            13) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.
    
            14) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.
    
            15) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 
    
            16) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 
    
            17) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 
    
            18) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 
    
            19) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 
    
            20) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 
    
            21) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 
    
            22) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 
    
            23) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                To change to a dashed line, users should set state_border_linestyle='--'. 
    
            24) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                To change to a dashed line, users should set county_border_linestyle='--'. 
    
            25) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                To change to a dashed line, users should set gacc_border_linestyle='--'. 
    
            26) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            27) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            28) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            29) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'.   
    
            Returns: A set of graphic showing forecast cross-sections between two points saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Two Point Cross Section/{reference_system}/{parameters}/
        
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        if north_to_south == False:
            ref = 'lon'
        else:
            ref = 'lat'
    
        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones
    
            state_border_linewidth = state_border_linewidth
            county_border_linewidth = county_border_linewidth
            gacc_border_linewidth = gacc_border_linewidth
            cwa_border_linewidth = cwa_border_linewidth
            nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
            nws_public_zones_linewidth = nws_public_zones_linewidth
            psa_border_linewidth = psa_border_linewidth
    
        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
                state_border_linewidth=1 
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                state_border_linewidth=1 
                county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
                gacc_border_linewidth=1
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
                cwa_border_linewidth=1
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                cwa_border_linewidth=1
                nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                cwa_border_linewidth=1
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                cwa_border_linewidth=1
                county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_public_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                cwa_border_linewidth=0.25
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                county_border_linewidth=0.25 
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                county_border_linewidth=0.25 

        start_lon = starting_point[1]
        start_lat = starting_point[0]
        end_lon = ending_point[1]
        end_lat = ending_point[0]

        if region == 'Custom' or region == 'custom':

            if start_lon < end_lon:
                western_bound = start_lon
                eastern_bound = end_lon
            else:
                eastern_bound = start_lon
                western_bound = end_lon
    
            if start_lat < end_lat:
                southern_bound = start_lat
                northern_bound = end_lat
            else:
                northern_bound = start_lat
                southern_bound = end_lat
                
            western_bound = western_bound - 1
            eastern_bound = eastern_bound + 1
            southern_bound = southern_bound - 1
            northern_bound = northern_bound + 1

        if data == False:
            if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                
        
            else:
                if model == 'RAP 32' or model == 'rap 32':
                    ds = model_data.get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                else:
                    ds = model_data.get_nomads_opendap_data(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                
                
        if data == True:

            ds = ds
    
        ds = ds.squeeze()
        if model == 'NAM' or model == 'RAP' or model == 'RAP 32':
            ds = ds.sel(lev=ds['lev'][0:21])
        if model == 'GFS0p25':
            ds = ds.sel(lev=ds['lev'][0:13])

        if model == 'GFS0p25' or model == 'RAP 32':
            ds['lon'] = (ds['lon'] - 360)
        else:
            pass

        sfc_pressure = ds['pressfc']/100
        gph_500 = (ds['hgtprs'][:, -1, :, :])/10
        u = (ds['ugrdprs']) * 2.23694
        v = (ds['vgrdprs']) * 2.23694
        ds['dwptprs'] = mpcalc.dewpoint_from_relative_humidity(ds['tmpprs'] * units('kelvin'), ds['rhprs'] * units('percent'))
        theta_e = mpcalc.equivalent_potential_temperature(ds['lev'] * units('hPa'), ds['tmpprs'] * units('kelvin'), ds['dwptprs']) 
        rh = ds['rhprs']
        vv = ds['vvelprs']
        
        cross = cross_section(vv, starting_point, ending_point)
        u_cross = cross_section(u, starting_point, ending_point)
        v_cross = cross_section(v, starting_point, ending_point)
        rh_cross = cross_section(rh, starting_point, ending_point)
        theta_e_cross = cross_section(theta_e, starting_point, ending_point)
        height_cross = cross_section(sfc_pressure, starting_point, ending_point)
        vv_grid, pressure, index, lon, height = xr.broadcast(cross, cross['lev'], cross['index'], cross[ref], height_cross) 

        path, path_print = file_functions.forecast_cross_sections_graphics_paths(model, 'Two Point Cross Section', 'Lower Atmosphere Theta-E & Wind Barbs', reference_system, start_coords=starting_point, end_coords=ending_point)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
                
        print(f"Any old images (if any) in {path_print} have been deleted.")

        stop_loop = len(ds['time']) - 1
        print(stop_loop)
        time = ds['time']
        times = time.to_pandas()

        cmap = colormaps.theta_e_colormap()

        if stop_loop >= 100:
            step = 2
        else:
            step = 1

        min_lon = np.nanmin(cross['lon'])
        max_lon = np.nanmax(cross['lon'])
        min_lat = np.nanmin(cross['lat'])
        max_lat = np.nanmax(cross['lat'])

        wb = min_lon - 6
        eb = max_lon + 6
        nb = max_lat + 3
        sb = min_lat - 3

        start_lon = starting_point[1]
        start_lat = starting_point[0]
        end_lon = ending_point[1]
        end_lat = ending_point[0]
    
        if start_lat >= 0:
            start_lat_symbol = '°N'
        else:
            start_lat_symbol = '°S'
            
        if end_lat >= 0:
            end_lat_symbol = '°N'
        else:
            end_lat_symbol = '°S'
    
        if start_lon <= 180:
            start_lon_symbol = '°W'
        else:
            start_lon_symbol = '°E'

        if end_lon <= 180:
            end_lon_symbol = '°W'
        else:
            end_lon_symbol = '°E'

        if model == 'GFS0p25':
            decimate = 1
        else:
            decimate = 2
    
        for i in range(0, stop_loop, step):

            try:

                step_c = 1
                start_c = round(np.nanmin(theta_e[:, i, :]),0)
                stop_c = (round(np.nanmax(theta_e[:, i, :]),0) + step_c)
    
                low = np.nanmin(vv[i, :, :])
                high = np.nanmax(vv[i, :, :])
        
                if low < 0 and high >= 0:
                    vv_range = abs(low) + high
                if low < 0 and high < 0 :
                    vv_range = low - high
                if low >= 0 and high >= 0:
                    vv_range = high - low
        
                step = round(vv_range/10, 1)
        
                if low < 0 and abs(low) > high and high >=0:
                    upper_bound = round(abs(low),2)
                    lower_bound = round(low,2)
                if low < 0 and high >= 0 and abs(low) <= high:
                    lower_bound = round((high * -1),2)
                    upper_bound = round(high,2)
                if low < 0 and high < 0:
                    upper_bound = round(high,2)
                    lower_bound = round(low,2)
                if low >= 0 and high >= 0:
                    upper_bound = round(high,2)
                    lower_bound = round(low,2)
                
                step_cs = round(vv_range/100, 2)
                                
        
                fname = f"Image_{i}.png"
    
    
                fig = plt.figure(figsize=(18, 7))
                gs = gridspec.GridSpec(10, 10)
                ax1 = fig.add_subplot(gs[0:10, 0:10])
                ax1.set_yscale('symlog')
                ax1.set_yticks(np.arange(1000, 50, -100))
                ax1.set_yticklabels(np.arange(1000, 50, -100))
                ax1.set_ylim(1000, 475)
                ax1.fill_between(lon[i, 0, :], height[i, 0, :], np.nanmax(sfc_pressure), color="black", zorder=10)
                ax1.contourf(lon[i, :, :], pressure[i, :, :], theta_e_cross[:, i, :], levels = np.arange(start_c, (stop_c + 3), 3), cmap=cmap, alpha=0.25, extend='both')
                
                c = ax1.contour(lon[i, :, :], pressure[i, :, :], theta_e_cross[:, i, :], levels = np.arange(start_c, (stop_c + 3), 3), colors='black', zorder=2, linewidths=1, linestyles='-')
                ax1.clabel(c, levels = np.arange(start_c, (stop_c + 3), 3), inline=True, fontsize=8, rightside_up=True)
                
                ax1.barbs(lon[i, ::decimate, ::decimate], pressure[i, ::decimate, ::decimate], u_cross[i, ::decimate, ::decimate], v_cross[i, ::decimate, ::decimate], clip_on=True, zorder=10, color='black', length=5, alpha=0.5)
                ax1.text(0.01, -0.08, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS | Map Reference System: "+reference_system, transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
                ax1.text(0.8, -0.08, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
    
                plt.title(f"{model.upper()} LOWER ATMOSPHERIC THETA-E [K] & WIND BARBS [MPH]\nSTART: {str(abs(start_lat))}{start_lat_symbol}/{str(abs(start_lon))}{start_lon_symbol} END: {str(abs(end_lat))}{end_lat_symbol}/{str(abs(end_lon))}{end_lon_symbol}\nFORECAST VALID: {times.iloc[i].strftime('%a %d/%H UTC')} | INITIALIZATION: {times.iloc[0].strftime('%a %d/%H UTC')}", fontsize=10, fontweight='bold', loc='left')
    
                ax2 = fig.add_subplot(gs[0:2, 8:10], projection=ccrs.PlateCarree())
                ax2.axis("off")
                ax2.set_extent([wb, eb, sb, nb], ccrs.PlateCarree())
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
                ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
                ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
                ax2.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
                if show_rivers == True:
                    ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
                else:
                    pass
            
                if show_gacc_borders == True:
                    ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                else:
                    pass
                if show_psa_borders == True:
                    ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                else:
                    pass
                if show_county_borders == True:
                    ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                else:
                    pass
                if show_state_borders == True:
                    ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                else:
                    pass
                if show_cwa_borders == True:
                    ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                else:
                    pass
                if show_nws_firewx_zones == True:
                    ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                else:
                    pass
                if show_nws_public_zones == True:
                    ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                else:
                    pass    
    
            
                ax2.plot(start_lon, start_lat, marker='*', markersize=8, color='k', zorder=15)
                ax2.plot(end_lon, end_lat, marker='*', markersize=8, color='k', zorder=15)
                ax2.plot(cross['lon'], cross['lat'], c='k', zorder=10)
                ax2.contourf(ds['lon'], ds['lat'], gph_500[i, :, :], levels=np.arange(480, 601, 1), cmap=colormaps.gph_colormap(), alpha=0.25, transform=datacrs, extend='both')
                ax2.set_title(f"500 MB GPH", fontweight='bold', fontsize=8)
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                print(f"Saved image for forecast {times.iloc[i].strftime('%a %d/%H UTC')} to {path_print}.")
                tim.sleep(10)
            except Exception as e:
                plt.close(fig)


    def plot_lower_atmosphere_theta_e_rh_vertical_velocity_wind(model, region, starting_point, ending_point, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', north_to_south=False):
    
        r'''
            This function plots forecast cross-sections between two points. Paramter: Lower Atmosphere Theta-E & RH & Wind Barbs. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) NAM - North American Model
                   3) RAP - RAP for the CONUS
                   4) RAP 32 - 32km North American RAP
    
            2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                                 To look at any state use the 2-letter abbreviation for the state in either all capitals
                                 or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                                 CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                                 North America use either: NA, na, North America or north america. If the user wishes to use custom
                                 boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                                 the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                                 'oscc' for South Ops. 

            3) starting_point (Tuple) - (lat,lon) in decimal degrees. 

            4) ending_point (Tuple) - (lat,lon) in decimal degrees.
    
            Optional Arguments:
    
            
            1) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                and passing the data in or if the function needs to download the data. A value of False means the data
                is downloaded inside of the function while a value of True means the user is downloading the data outside
                of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                things, it is recommended to set this value to True and download the data outside of the function and pass
                it in so that the amount of data requests on the host servers can be minimized. 
    
    
            2) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

            3) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


            4) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


            5) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                         

            6) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                         custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
    
            7) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                     wishes to use a reference system not on this list, please see items 17-23. 
                
                Reference Systems: 
                
                1) 'States & Counties'
                2) 'States Only'
                3) 'GACC Only'
                4) 'GACC & PSA'
                5) 'CWA Only'
                6) 'NWS CWAs & NWS Public Zones'
                7) 'NWS CWAs & NWS Fire Weather Zones'
                8) 'NWS CWAs & Counties'
                9) 'GACC & PSA & NWS Fire Weather Zones'
                10) 'GACC & PSA & NWS Public Zones'
                11) 'GACC & PSA & NWS CWA'
                12) 'GACC & PSA & Counties'
                13) 'GACC & Counties'
    
    
            8) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide state borders. 
    
            9) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide county borders. 
    
            10) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display GACC borders. 
    
            11) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display PSA borders.
    
            12) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display CWA borders.
    
            13) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.
    
            14) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.
    
            15) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 
    
            16) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 
    
            17) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 
    
            18) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 
    
            19) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 
    
            20) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 
    
            21) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 
    
            22) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 
    
            23) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                To change to a dashed line, users should set state_border_linestyle='--'. 
    
            24) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                To change to a dashed line, users should set county_border_linestyle='--'. 
    
            25) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                To change to a dashed line, users should set gacc_border_linestyle='--'. 
    
            26) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            27) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            28) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            29) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'.   
    
            Returns: A set of graphic showing forecast cross-sections between two points saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Two Point Cross Section/{reference_system}/{parameters}/
        
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        if north_to_south == False:
            ref = 'lon'
        else:
            ref = 'lat'
    
        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones
    
            state_border_linewidth = state_border_linewidth
            county_border_linewidth = county_border_linewidth
            gacc_border_linewidth = gacc_border_linewidth
            cwa_border_linewidth = cwa_border_linewidth
            nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
            nws_public_zones_linewidth = nws_public_zones_linewidth
            psa_border_linewidth = psa_border_linewidth
    
        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
                state_border_linewidth=1 
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                state_border_linewidth=1 
                county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
                gacc_border_linewidth=1
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
                cwa_border_linewidth=1
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                cwa_border_linewidth=1
                nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                cwa_border_linewidth=1
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                cwa_border_linewidth=1
                county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_public_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                cwa_border_linewidth=0.25
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                county_border_linewidth=0.25 
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                county_border_linewidth=0.25 

        start_lon = starting_point[1]
        start_lat = starting_point[0]
        end_lon = ending_point[1]
        end_lat = ending_point[0]

        if region == 'Custom' or region == 'custom':

            if start_lon < end_lon:
                western_bound = start_lon
                eastern_bound = end_lon
            else:
                eastern_bound = start_lon
                western_bound = end_lon
    
            if start_lat < end_lat:
                southern_bound = start_lat
                northern_bound = end_lat
            else:
                northern_bound = start_lat
                southern_bound = end_lat
                
            western_bound = western_bound - 1
            eastern_bound = eastern_bound + 1
            southern_bound = southern_bound - 1
            northern_bound = northern_bound + 1

        if data == False:
            if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                
        
            else:
                if model == 'RAP 32' or model == 'rap 32':
                    ds = model_data.get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                else:
                    ds = model_data.get_nomads_opendap_data(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                
                
        if data == True:

            ds = ds
    
        ds = ds.squeeze()
        if model == 'NAM' or model == 'RAP' or model == 'RAP 32':
            ds = ds.sel(lev=ds['lev'][0:21])
        if model == 'GFS0p25':
            ds = ds.sel(lev=ds['lev'][0:13])

        if model == 'GFS0p25' or model == 'RAP 32':
            ds['lon'] = (ds['lon'] - 360)
        else:
            pass

        sfc_pressure = ds['pressfc']/100
        gph_500 = (ds['hgtprs'][:, -1, :, :])/10
        u = (ds['ugrdprs']) * 2.23694
        v = (ds['vgrdprs']) * 2.23694
        ds['dwptprs'] = mpcalc.dewpoint_from_relative_humidity(ds['tmpprs'] * units('kelvin'), ds['rhprs'] * units('percent'))
        theta_e = mpcalc.equivalent_potential_temperature(ds['lev'] * units('hPa'), ds['tmpprs'] * units('kelvin'), ds['dwptprs']) 
        rh = ds['rhprs']
        vv = ds['vvelprs']
        
        cross = cross_section(vv, starting_point, ending_point)
        u_cross = cross_section(u, starting_point, ending_point)
        v_cross = cross_section(v, starting_point, ending_point)
        rh_cross = cross_section(rh, starting_point, ending_point)
        theta_e_cross = cross_section(theta_e, starting_point, ending_point)
        height_cross = cross_section(sfc_pressure, starting_point, ending_point)
        vv_grid, pressure, index, lon, height = xr.broadcast(cross, cross['lev'], cross['index'], cross[ref], height_cross) 

    
        path, path_print = file_functions.forecast_cross_sections_graphics_paths(model, 'Two Point Cross Section', 'Lower Atmosphere Theta-E & RH & Wind Barbs', reference_system, start_coords=starting_point, end_coords=ending_point)

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
                
        print(f"Any old images (if any) in {path_print} have been deleted.")

        stop_loop = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()

        cmap = colormaps.vertical_velocity_colormap()

        if stop_loop >= 100:
            step = 2
        else:
            step = 1

        min_lon = np.nanmin(cross['lon'])
        max_lon = np.nanmax(cross['lon'])
        min_lat = np.nanmin(cross['lat'])
        max_lat = np.nanmax(cross['lat'])

        wb = min_lon - 6
        eb = max_lon + 6
        nb = max_lat + 3
        sb = min_lat - 3

        start_lon = starting_point[1]
        start_lat = starting_point[0]
        end_lon = ending_point[1]
        end_lat = ending_point[0]
    
        if start_lat >= 0:
            start_lat_symbol = '°N'
        else:
            start_lat_symbol = '°S'
            
        if end_lat >= 0:
            end_lat_symbol = '°N'
        else:
            end_lat_symbol = '°S'
    
        if start_lon <= 180:
            start_lon_symbol = '°W'
        else:
            start_lon_symbol = '°E'

        if end_lon <= 180:
            end_lon_symbol = '°W'
        else:
            end_lon_symbol = '°E'

        if model == 'GFS0p25':
            decimate = 1
        else:
            decimate = 2
    
        for i in range(0, stop_loop, step):

            try:

                step_c = 1
                start_c = round(np.nanmin(theta_e[:, i, :]),0)
                stop_c = (round(np.nanmax(theta_e[:, i, :]),0) + step_c)
    
                low = np.nanmin(vv[i, :, :])
                high = np.nanmax(vv[i, :, :])
        
                if low < 0 and high >= 0:
                    vv_range = abs(low) + high
                if low < 0 and high < 0 :
                    vv_range = low - high
                if low >= 0 and high >= 0:
                    vv_range = high - low
        
                step = round(vv_range/10, 1)
        
                if low < 0 and abs(low) > high and high >=0:
                    upper_bound = round(abs(low),2)
                    lower_bound = round(low,2)
                if low < 0 and high >= 0 and abs(low) <= high:
                    lower_bound = round((high * -1),2)
                    upper_bound = round(high,2)
                if low < 0 and high < 0:
                    upper_bound = round(high,2)
                    lower_bound = round(low,2)
                if low >= 0 and high >= 0:
                    upper_bound = round(high,2)
                    lower_bound = round(low,2)
                
                step_cs = round(vv_range/100, 2)
                                
        
                fname = f"Image_{i}.png"
    
    
                fig = plt.figure(figsize=(18, 7))
                gs = gridspec.GridSpec(10, 10)
                ax1 = fig.add_subplot(gs[0:10, 0:10])
                ax1.set_yscale('symlog')
                ax1.set_yticks(np.arange(1000, 50, -100))
                ax1.set_yticklabels(np.arange(1000, 50, -100))
                ax1.set_ylim(1000, 475)
                ax1.fill_between(lon[i, 0, :], height[i, 0, :], np.nanmax(sfc_pressure), color="black", zorder=10)
                ax1.contourf(lon[i, :, :], pressure[i, :, :], vv_grid[i, :, :], levels=np.arange(lower_bound, (upper_bound + step_cs), step_cs), cmap=cmap, alpha=0.25, extend='both')
                c = ax1.contour(lon[i, :, :], pressure[i, :, :], theta_e_cross[:, i, :], levels = np.arange(start_c, (stop_c + 3), 3), colors='black', zorder=2, linewidths=1, linestyles='-')
                ax1.clabel(c, levels = np.arange(start_c, (stop_c + 3), 3), inline=True, fontsize=8, rightside_up=True)
                c1 = ax1.contour(lon[i, :, :], pressure[i, :, :], rh_cross[i, :, :], levels = np.arange(0, 110, 10), colors='green', zorder=2, linewidths=1, linestyles='--')
                ax1.clabel(c1, levels = np.arange(0, 110, 10), inline=True, fontsize=8, rightside_up=True)
                
                ax1.barbs(lon[i, ::decimate, ::decimate], pressure[i, ::decimate, ::decimate], u_cross[i, ::decimate, ::decimate], v_cross[i, ::decimate, ::decimate], clip_on=True, zorder=10, color='black', length=5, alpha=0.5)
                ax1.text(0.01, -0.08, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS | Map Reference System: "+reference_system, transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
                ax1.text(0.8, -0.08, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
    
                plt.title(f"{model.upper()} LOWER ATMOSPHERIC VERTICAL VELOCITY (SHADED) [Pa/s] & THETA-E [K] (SOLID CONTOURS) & RH [%] (DASHED CONTOURS) & WIND BARBS [MPH]\nSTART: {str(abs(start_lat))}{start_lat_symbol}/{str(abs(start_lon))}{start_lon_symbol} END: {str(abs(end_lat))}{end_lat_symbol}/{str(abs(end_lon))}{end_lon_symbol}\nFORECAST VALID: {times.iloc[i].strftime('%a %d/%H UTC')} | INITIALIZATION: {times.iloc[0].strftime('%a %d/%H UTC')}", fontsize=10, fontweight='bold', loc='left')
    
                ax2 = fig.add_subplot(gs[0:2, 8:10], projection=ccrs.PlateCarree())
                ax2.axis("off")
                ax2.set_extent([wb, eb, sb, nb], ccrs.PlateCarree())
                ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
                ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
                ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
                ax2.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
                if show_rivers == True:
                    ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
                else:
                    pass
            
                if show_gacc_borders == True:
                    ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                else:
                    pass
                if show_psa_borders == True:
                    ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                else:
                    pass
                if show_county_borders == True:
                    ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                else:
                    pass
                if show_state_borders == True:
                    ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                else:
                    pass
                if show_cwa_borders == True:
                    ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                else:
                    pass
                if show_nws_firewx_zones == True:
                    ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                else:
                    pass
                if show_nws_public_zones == True:
                    ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                else:
                    pass    
    
            
                ax2.plot(start_lon, start_lat, marker='*', markersize=8, color='k', zorder=15)
                ax2.plot(end_lon, end_lat, marker='*', markersize=8, color='k', zorder=15)
                ax2.plot(cross['lon'], cross['lat'], c='k', zorder=10)
                ax2.contourf(ds['lon'], ds['lat'], gph_500[i, :, :], levels=np.arange(480, 601, 1), cmap=colormaps.gph_colormap(), alpha=0.25, transform=datacrs, extend='both')
                ax2.set_title(f"500 MB GPH", fontweight='bold', fontsize=8)
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                print(f"Saved image for forecast {times.iloc[i].strftime('%a %d/%H UTC')} to {path_print}.")
                tim.sleep(10)
            except Exception as e:
                plt.close(fig)



    def plot_favorable_firewx_forecast(model, region, starting_point, ending_point, low_rh_threshold=15, high_wind_threshold=25, high_temperature_threshold=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, data=False, ds=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', north_to_south=False):
    
        r'''
            This function plots a time vs. pressure cross-section forecast for a given point. Paramters: Lower Atmosphere Favorable Fire Weather Forecast. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) NAM - North American Model
                   3) RAP - RAP for the CONUS
                   4) RAP 32 - 32km North American RAP
    
            2) station_id (String) - The 4-letter airport station identifier. 
                                     If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 

            3) save_name (String) - The name at which you want to name your graphics file. For example if I was creating a time cross-section for 
                                    Ontario International Airport in Ontario, California I would name the file "KONT.png" as KONT is the station ID. 
    
            Optional Arguments:

            1) low_rh_threshold (Integer) - Default = 15. The threshold for the contour line that defines what extremely low relative humidity is.

            2) high_wind_threshold (Integer) - Default = 25. The threshold for the contour line that defines what high winds are.

            3) temperature_threshold (Integer) - Default = None. This is to be used if the user wishes to add temperature as a factor to what 
               defines favorable fire weather conditions. When set to None, only RH & Wind Speed/Gust are taken 
               into account. When set to an integer value, the temperature will also be taken into account. 

            4) longitude (Float or Integer) - Default = None. The longitude of the point in decimal degrees. 
            
            5) latitude (Float or Integer) - Default = None. The latitude of the point in decimal degrees. 
            
            6) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                and passing the data in or if the function needs to download the data. A value of False means the data
                is downloaded inside of the function while a value of True means the user is downloading the data outside
                of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                things, it is recommended to set this value to True and download the data outside of the function and pass
                it in so that the amount of data requests on the host servers can be minimized. 
    
    
            7) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 
    
            8) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
                                                                     wishes to use a reference system not on this list, please see items 17-23. 
                
                Reference Systems: 
                
                1) 'States & Counties'
                2) 'States Only'
                3) 'GACC Only'
                4) 'GACC & PSA'
                5) 'CWA Only'
                6) 'NWS CWAs & NWS Public Zones'
                7) 'NWS CWAs & NWS Fire Weather Zones'
                8) 'NWS CWAs & Counties'
                9) 'GACC & PSA & NWS Fire Weather Zones'
                10) 'GACC & PSA & NWS Public Zones'
                11) 'GACC & PSA & NWS CWA'
                12) 'GACC & PSA & Counties'
                13) 'GACC & Counties'
    
    
            9) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide state borders. 
    
            10) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
                Default setting is False. Users should change this value to False if they wish to hide county borders. 
    
            11) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display GACC borders. 
    
            12) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display PSA borders.
    
            13) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display CWA borders.
    
            14) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.
    
            15) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
                Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.
    
            16) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 
    
            17) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 
    
            18) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 
    
            19) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 
    
            20) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 
    
            21) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 
    
            22) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 
    
            23) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 
    
            24) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
                To change to a dashed line, users should set state_border_linestyle='--'. 
    
            25) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
                To change to a dashed line, users should set county_border_linestyle='--'. 
    
            26) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
                To change to a dashed line, users should set gacc_border_linestyle='--'. 
    
            27) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            28) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            29) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'. 
    
            30) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
                To change to a dashed line, users should set psa_border_linestyle='--'.   
    
            Returns: A graphic showing a time vs. pressure cross section for a point saved to path: f:Weather Data/Forecast Model Data/{model}/Cross Sections/Time Cross Section/{reference_system}/{parameters}/{save_name}
        '''
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        if north_to_south == False:
            ref = 'lon'
        else:
            ref='lat'
    
        if reference_system == 'Custom' or reference_system == 'custom':
            show_state_borders = show_state_borders
            show_county_borders = show_county_borders
            show_gacc_borders = show_gacc_borders
            show_psa_borders = show_psa_borders
            show_cwa_borders = show_cwa_borders
            show_nws_firewx_zones = show_nws_firewx_zones
            show_nws_public_zones = show_nws_public_zones
    
            state_border_linewidth = state_border_linewidth
            county_border_linewidth = county_border_linewidth
            gacc_border_linewidth = gacc_border_linewidth
            cwa_border_linewidth = cwa_border_linewidth
            nws_firewx_zones_linewidth = nws_firewx_zones_linewidth
            nws_public_zones_linewidth = nws_public_zones_linewidth
            psa_border_linewidth = psa_border_linewidth
    
        if reference_system != 'Custom' and reference_system != 'custom':
            
            show_state_borders = False
            show_county_borders = False
            show_gacc_borders = False
            show_psa_borders = False
            show_cwa_borders = False
            show_nws_firewx_zones = False
            show_nws_public_zones = False
    
            if reference_system == 'States Only':
                show_state_borders = True
                state_border_linewidth=1 
            if reference_system == 'States & Counties':
                show_state_borders = True
                show_county_borders = True
                state_border_linewidth=1 
                county_border_linewidth=0.25
            if reference_system == 'GACC Only':
                show_gacc_borders = True
                gacc_border_linewidth=1
            if reference_system == 'GACC & PSA':
                show_gacc_borders = True
                show_psa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.25
            if reference_system == 'CWA Only':
                show_cwa_borders = True
                cwa_border_linewidth=1
            if reference_system == 'NWS CWAs & NWS Public Zones':
                show_cwa_borders = True
                show_nws_public_zones = True
                cwa_border_linewidth=1
                nws_public_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & NWS Fire Weather Zones':
                show_cwa_borders = True
                show_nws_firewx_zones = True
                cwa_border_linewidth=1
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'NWS CWAs & Counties':
                show_cwa_borders = True
                show_county_borders = True
                cwa_border_linewidth=1
                county_border_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Fire Weather Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_firewx_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_firewx_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS Public Zones':
                show_gacc_borders = True
                show_psa_borders = True
                show_nws_public_zones = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                nws_public_zones_linewidth=0.25
            if reference_system == 'GACC & PSA & NWS CWA':
                show_gacc_borders = True
                show_psa_borders = True
                show_cwa_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                cwa_border_linewidth=0.25
            if reference_system == 'GACC & PSA & Counties':
                show_gacc_borders = True
                show_psa_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                psa_border_linewidth=0.5
                county_border_linewidth=0.25 
            if reference_system == 'GACC & Counties':
                show_gacc_borders = True
                show_county_borders = True
                gacc_border_linewidth=1
                county_border_linewidth=0.25 
        start_lon = starting_point[1]
        start_lat = starting_point[0]
        end_lon = ending_point[1]
        end_lat = ending_point[0]

        if region == 'Custom' or region == 'custom':

            if start_lon < end_lon:
                western_bound = start_lon
                eastern_bound = end_lon
            else:
                eastern_bound = start_lon
                western_bound = end_lon
    
            if start_lat < end_lat:
                southern_bound = start_lat
                northern_bound = end_lat
            else:
                northern_bound = start_lat
                southern_bound = end_lat

            western_bound = western_bound - 1
            eastern_bound = eastern_bound + 1
            southern_bound = southern_bound - 1
            northern_bound = northern_bound + 1

        if data == False:
            if model == 'RAP' or model == 'rap' or model == 'Eastern North Pacific RAP' or model == 'eastern north pacific rap':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                
        
            else:
                if model == 'RAP 32' or model == 'rap 32':
                    ds = model_data.get_hourly_rap_data_area_forecast(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                else:
                    ds = model_data.get_nomads_opendap_data(model, region, western_bound, eastern_bound, southern_bound, northern_bound)
                
                
        if data == True:

            ds = ds
    
        ds = ds.squeeze()
        if model == 'NAM' or model == 'RAP' or model == 'RAP 32':
            ds = ds.sel(lev=ds['lev'][0:21])
        if model == 'GFS0p25':
            ds = ds.sel(lev=ds['lev'][0:13])

        if model == 'GFS0p25' or model == 'RAP 32':
            ds['lon'] = (ds['lon'] - 360)
        else:
            pass
    
    
        path, path_print = file_functions.forecast_cross_sections_graphics_paths(model, 'Two Point Cross Section', 'Lower Atmosphere Favorable Fire Weather Forecast', reference_system, start_coords=starting_point, end_coords=ending_point)
    
        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
    
        print(f"Any old images (if any) in {path_print} have been deleted.")
    
        cmap = colormaps.red_flag_warning_criteria_colormap()
    
        u = (ds['ugrdprs']) * 2.23694
        v = (ds['vgrdprs']) * 2.23694
        ws = np.hypot(u,v)
        gph_500 = (ds['hgtprs'][:, -1, :, :])/10
        
        time = ds['time']
        times = time.to_pandas()
        sfc_pressure = (ds['pressfc'][:]) / 100
        pressure = ds['ugrdprs']['lev']
        height_ft = (ds['hgtprs'][:, :]) * 3.28084
        height_sfc = (ds['hgtsfc'][:])  * 3.28084
        height_agl = height_ft - height_sfc
        pressure_grid, time_grid = np.meshgrid(pressure, time)
        temperature = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmpprs'])
        rh = ds['rhprs']
        
        u_cross = cross_section(u, starting_point, ending_point)
        v_cross = cross_section(v, starting_point, ending_point)
        rh_cross = cross_section(rh, starting_point, ending_point)
        ws_cross = cross_section(ws, starting_point, ending_point)
        height_cross = cross_section(sfc_pressure, starting_point, ending_point)
        ws_cross, pressure, index, lon, height = xr.broadcast(ws_cross, u_cross['lev'], u_cross['index'], u_cross[ref], height_cross) 

        if high_temperature_threshold == None:
            mask = (rh_cross <= low_rh_threshold) & (ws_cross >= high_wind_threshold)
        else:
            temp_cross = cross_section(temperature, starting_point, ending_point)
            mask = (rh_cross <= low_rh_threshold) & (ws_cross >= high_wind_threshold) & (temp_cross >= high_temperature_threshold)

        stop_loop = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()

        if stop_loop >= 100:
            step = 2
        else:
            step = 1

        min_lon = np.nanmin(u_cross['lon'])
        max_lon = np.nanmax(u_cross['lon'])
        min_lat = np.nanmin(u_cross['lat'])
        max_lat = np.nanmax(u_cross['lat'])

        wb = min_lon - 6
        eb = max_lon + 6
        nb = max_lat + 3
        sb = min_lat - 3

        start_lon = starting_point[1]
        start_lat = starting_point[0]
        end_lon = ending_point[1]
        end_lat = ending_point[0]
    
        if start_lat >= 0:
            start_lat_symbol = '°N'
        else:
            start_lat_symbol = '°S'
            
        if end_lat >= 0:
            end_lat_symbol = '°N'
        else:
            end_lat_symbol = '°S'
    
        if start_lon <= 180:
            start_lon_symbol = '°W'
        else:
            start_lon_symbol = '°E'

        if end_lon <= 180:
            end_lon_symbol = '°W'
        else:
            end_lon_symbol = '°E'

        if model == 'GFS0p25':
            decimate = 1
        else:
            decimate = 2
    
        for i in range(0, stop_loop, step):
                            
    
            fname = f"Image_{i}.png"

            fig = plt.figure(figsize=(18, 7))
            gs = gridspec.GridSpec(10, 10)
            ax1 = fig.add_subplot(gs[0:10, 0:10])
            ax1.set_yscale('symlog')
            ax1.set_yticks(np.arange(1000, 50, -100))
            ax1.set_yticklabels(np.arange(1000, 50, -100))
            ax1.set_ylim(1000, 475)
            ax1.fill_between(lon[i, 0, :], height[i, 0, :], np.nanmax(sfc_pressure), color="black", zorder=10)
            try:
                ax1.pcolormesh(lon[i, :, :], pressure[i, :, :], mask[i, :, :], cmap=cmap, alpha=0.25)
            except Exception as e:
                pass
            c = ax1.contour(lon[i, :, :], pressure[i, :, :], rh_cross[i, :, :], levels = np.arange(0, 110, 10), colors='green', zorder=2, linewidths=1, linestyles='-')
            ax1.clabel(c, levels = np.arange(0, 110, 10), inline=True, fontsize=8, rightside_up=True)
            c1 = ax1.contour(lon[i, :, :], pressure[i, :, :], ws_cross[i, :, :], levels = np.arange(0, (np.nanmax(ws[i, :, :]) + 5), 5), colors='darkorange', zorder=2, linewidths=1, linestyles='dotted')
            ax1.clabel(c1, levels = np.arange(0, (np.nanmax(ws[i, :, :]) + 5), 5), inline=True, fontsize=8, rightside_up=True)
            if high_temperature_threshold != None:
    
    
                c3 = ax1.contour(lon[i, :, :], pressure[i, :, :], temp_cross[i, :, :], levels = np.arange(0, (int(round(np.nanmax(temperature),0)) + 5), 5), colors='darkred', zorder=2, linewidths=1, linestyles='dashdot')
                ax1.clabel(c3, levels = np.arange(0, (int(round(np.nanmax(temperature),0)) + 5), 5), inline=True, fontsize=8, rightside_up=True)      
    
            else:
                pass
            
            
            ax1.barbs(lon[i, ::decimate, ::decimate], pressure[i, ::decimate, ::decimate], u_cross[i, ::decimate, ::decimate], v_cross[i, ::decimate, ::decimate], clip_on=True, zorder=10, color='black', length=5, alpha=0.5)
            ax1.text(0.01, -0.08, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS | Map Reference System: "+reference_system, transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax1.text(0.8, -0.08, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax1.transAxes, fontsize=6, fontweight='bold', bbox=props)

            if high_temperature_threshold == None:
                plt.title(f"{model.upper()} LOWER ATMOSPHERIC FAVORABLE FIREWX FORECAST (SHADED RED) -> RH <= {low_rh_threshold} [%] & WIND SPEED >= {high_wind_threshold} [MPH]\nWIND SPEED (ORANGE CONTOURS) | RH (GREEN CONTOURS)\nSTART: {str(abs(start_lat))}{start_lat_symbol}/{str(abs(start_lon))}{start_lon_symbol} END: {str(abs(end_lat))}{end_lat_symbol}/{str(abs(end_lon))}{end_lon_symbol}\nFORECAST VALID: {times.iloc[i].strftime('%a %d/%H UTC')} | INITIALIZATION: {times.iloc[0].strftime('%a %d/%H UTC')}", fontsize=10, fontweight='bold', loc='left')

            else:
                plt.title(f"{model.upper()} LOWER ATMOSPHERIC FAVORABLE FIREWX FORECAST (SHADED RED) -> T >= {high_temperature_threshold} [°F] & RH <= {low_rh_threshold} [%] & WIND SPEED >= {high_wind_threshold} [MPH]\nTEMPERATURE (RED CONTOURS) | WIND SPEED (ORANGE CONTOURS) | RH (GREEN CONTOURS)\nSTART: {str(abs(start_lat))}{start_lat_symbol}/{str(abs(start_lon))}{start_lon_symbol} END: {str(abs(end_lat))}{end_lat_symbol}/{str(abs(end_lon))}{end_lon_symbol}\nFORECAST VALID: {times.iloc[i].strftime('%a %d/%H UTC')} | INITIALIZATION: {times.iloc[0].strftime('%a %d/%H UTC')}", fontsize=10, fontweight='bold', loc='left')                

            ax2 = fig.add_subplot(gs[0:2, 8:10], projection=ccrs.PlateCarree())
            ax2.axis("off")
            ax2.set_extent([wb, eb, sb, nb], ccrs.PlateCarree())
            ax2.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax2.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax2.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax2.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax2.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax2.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax2.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax2.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax2.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax2.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax2.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax2.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax2.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass    

        
            ax2.plot(start_lon, start_lat, marker='*', markersize=8, color='k', zorder=15)
            ax2.plot(end_lon, end_lat, marker='*', markersize=8, color='k', zorder=15)
            ax2.plot(u_cross['lon'], u_cross['lat'], c='k', zorder=10)
            ax2.contourf(ds['lon'], ds['lat'], gph_500[i, :, :], levels=np.arange(480, 601, 1), cmap=colormaps.gph_colormap(), alpha=0.25, transform=datacrs, extend='both')
            ax2.set_title(f"500 MB GPH", fontweight='bold', fontsize=8)

            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            plt.close(fig)
            print(f"Saved image for forecast {times.iloc[i].strftime('%a %d/%H UTC')} to {path_print}.")
            tim.sleep(10)





