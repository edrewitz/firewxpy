
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

from matplotlib.patheffects import withStroke
from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from dateutil import tz
from firewxpy.calc import scaling, Thermodynamics, unit_conversion
from firewxpy.utilities import file_functions
from metpy.units import units
from firewxpy.data_access import model_data, station_coords

mpl.rcParams['xtick.labelsize'] = 6
mpl.rcParams['ytick.labelsize'] = 6
mpl.rcParams['font.weight'] = 'bold'
local_time, utc_time = standard.plot_creation_time()

datacrs = ccrs.PlateCarree()

provinces = cfeature.NaturalEarthFeature(category='cultural', 
    name='admin_1_states_provinces_lines', scale='50m', facecolor='none', edgecolor='k')

PSAs = geometry.import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", 'black', 'psa')

GACC = geometry.import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black', 'gacc')

CWAs = geometry.import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", 'black', 'cwa')

FWZs = geometry.import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", 'black', 'fwz')

PZs = geometry.import_shapefiles(f"NWS Public Zones/z_05mr24.shp", 'black', 'pz')

props = dict(boxstyle='round', facecolor='wheat', alpha=1)

class time_cross_sections:

    r'''
    This class hosts time vs. height cross-sections of a specific parameter for a specific point. 
    Motivated by Dr. Brian Tang's WxChallenge Model Guidance page: https://www.atmos.albany.edu/facstaff/tang/forecast/

    '''

    def plot_lower_atmosphere_wind(model, station_id, save_name, longitude=None, latitude=None, data=False, ds=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-'):
    
        r'''
            This function plots the vertical profile forecasts for a given point and shows the transport wind and precipitation forecast in the vicinity of the point. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) GFS0p25_1h - GFS 0.25x0.25 degree with 1 hour intervals
                   3) GFS0p50 - GFS 0.5x0.5 degree
                   4) GFS1p00 - GFS 1.0x1.0 degree
                   5) NAM - North American Model
                   6) NAM 1hr - North American Model with 1 hour intervals 
                   7) RAP - RAP for the CONUS
                   8) RAP 32 - 32km North American RAP
    
            2) station_id (String) - The 4-letter airport station identifier. 
                                     If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 
    
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
    
            Returns: A set of forecast vertical profile graphics saved to f:Weather Data/Forecast Model Data/{model}/Soundings/{latitude}{lat_symbol}/{longitude}{lon_symbol}/{reference_system}
        
        '''
    
    
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
    
        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
    
        print(f"Any old images (if any) in {path_print} have been deleted.")
    
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
        
    
        #mixing_heights = ds['hpblsfc']
        #mixing_heights_grid, time_grid = np.meshgrid(mixing_heights, time)
        
        fig = plt.figure(figsize=(18, 7))
        fig.set_facecolor('aliceblue')
        gs = gridspec.GridSpec(10, 10)
    
        ax1 = fig.add_subplot(gs[0:10, 0:10])
        
        ax1.set_yscale('symlog')
        ax1.set_yticks(np.arange(1000, 50, -100))
        ax1.set_yticklabels(np.arange(1000, 50, -100))
        ax1.set_ylim(np.nanmax(sfc_pressure), np.nanmax(sfc_pressure) - 300)
        ax1.xaxis.set_major_formatter(md.DateFormatter('%d/%HZ'))
        ax1.set_xticks(time)
                            
        ax1.contourf(time_grid, pressure_grid, ws[0:29, :], levels=np.arange(0, 71, 1), cmap=cmap, alpha=0.25, extend='max')
        c10 = ax1.contour(time_grid, pressure_grid, ws[0:29, :], levels=np.arange(0, 80, 10), colors='black', zorder=2, linewidths=1)
        ax1.clabel(c10, levels=np.arange(0, 80, 10), inline=True, fontsize=8, rightside_up=True)
        c5 = ax1.contour(time_grid, pressure_grid, ws[0:29, :], levels=np.arange(5, 85, 10), colors='black', zorder=2, linewidths=1, linestyles='--')
        ax1.clabel(c5, levels=np.arange(5, 85, 10), inline=True, fontsize=8, rightside_up=True)
        ax1.barbs(time_grid, pressure_grid, u[0:29, :], v[0:29, :], clip_on=True, zorder=10, color='black', length=5, alpha=0.5)
        if station_id != 'Custom' or station_id != 'custom':
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: WIND SPEED [MPH]\nSTATION: {station_id.upper()} - LAT: {str(lat)}{lat_symbol} | LON: {str(lon)}{lon_symbol}", fontsize=10, fontweight='bold', loc='left')
        else:
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: WIND SPEED [MPH]\nLAT: {str(lat)}{lat_symbol} | LON: {str(lon)}{lon_symbol}", fontsize=10, fontweight='bold', loc='left')
        plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[28].strftime('%a %d/%HZ')}", fontsize=8, fontweight='bold', loc='right')
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
        print(f"Saved image of cross-section to {path_print}/{save_name}.")


    def plot_lower_atmosphere_vertical_velocity(model, station_id, save_name, longitude=None, latitude=None, data=False, ds=None, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, show_rivers=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-'):
    
        r'''
            This function plots the vertical profile forecasts for a given point and shows the transport wind and precipitation forecast in the vicinity of the point. 
    
            Required Arguments:
    
            1) model (String) - This is the model the user must select. 
                                   
                   Here are the choices: 
                   1) GFS0p25 - GFS 0.25x0.25 degree
                   2) GFS0p25_1h - GFS 0.25x0.25 degree with 1 hour intervals
                   3) GFS0p50 - GFS 0.5x0.5 degree
                   4) GFS1p00 - GFS 1.0x1.0 degree
                   5) NAM - North American Model
                   6) NAM 1hr - North American Model with 1 hour intervals 
                   7) RAP - RAP for the CONUS
                   8) RAP 32 - 32km North American RAP
    
            2) station_id (String) - The 4-letter airport station identifier. 
                                     If the user wants to choose a custom point that is not an airport - enter: 'Custom' or 'custom'. 
    
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
    
            Returns: A set of forecast vertical profile graphics saved to f:Weather Data/Forecast Model Data/{model}/Soundings/{latitude}{lat_symbol}/{longitude}{lon_symbol}/{reference_system}
        
        '''
    
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
    
        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
    
        print(f"Any old images (if any) in {path_print} have been deleted.")
    
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
        ax1.set_ylim(np.nanmax(sfc_pressure), np.nanmax(sfc_pressure) - 300)
        ax1.xaxis.set_major_formatter(md.DateFormatter('%d/%HZ'))
        ax1.set_xticks(time)
                            
        ax1.contourf(time_grid, pressure_grid, vv[0:29, :], levels=np.arange(round(float(np.nanmin(vv[0:29, :])),2), round(float(np.nanmax(vv[0:29, :])),2) + 0.01, 0.01), cmap=cmap, alpha=0.25, extend='both')
        c10 = ax1.contour(time_grid, pressure_grid, vv[0:29, :], levels=np.arange(((round(float(np.nanmin(vv[0:29, :])),1)/0.1) * 0.1), ((round(float(np.nanmax(vv[0:29, :])),1)/0.1) * 0.1) + 0.1, 0.1), colors='black', zorder=2, linewidths=1)
        ax1.clabel(c10, levels=np.arange(((round(float(np.nanmin(vv[0:29, :])),1)/0.1) * 0.1), ((round(float(np.nanmax(vv[0:29, :])),1)/0.1) * 0.1) + 0.1, 0.1), inline=True, fontsize=8, rightside_up=True)
        c5 = ax1.contour(time_grid, pressure_grid, vv[0:29, :], levels=np.arange(((round(float(np.nanmin(vv[0:29, :])),1)/0.05) * 0.05), ((round(float(np.nanmax(vv[0:29, :])),1)/0.05) * 0.05) + 0.05, 0.05), colors='black', zorder=2, linewidths=1, linestyles='--')
        ax1.clabel(c5, levels=np.arange(((round(float(np.nanmin(vv[0:29, :])),1)/0.05) * 0.05), ((round(float(np.nanmax(vv[0:29, :])),1)/0.05) * 0.05) + 0.05, 0.05), inline=True, fontsize=8, rightside_up=True)
        if station_id != 'Custom' or station_id != 'custom':
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: VERTICAL VELOCITY [Pa/s]\nSTATION: {station_id.upper()} - LAT: {str(lat)}{lat_symbol} | LON: {str(lon)}{lon_symbol}", fontsize=10, fontweight='bold', loc='left')
        else:
            plt.title(f"{model.upper()} TIME VS. PRESSURE CROSS-SECTION: VERTICAL VELOCITY [Pa/s]\nLAT: {str(lat)}{lat_symbol} | LON: {str(lon)}{lon_symbol}", fontsize=10, fontweight='bold', loc='left')
        plt.title(f"VALID: {times[0].strftime('%a %d/%HZ')}-{times[28].strftime('%a %d/%HZ')}", fontsize=8, fontweight='bold', loc='right')
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
        print(f"Saved image of cross-section to {path_print}/{save_name}.")

