"""
This file has all the regular forecast model graphics on maps. 

(C) Eric J. Drewitz 2025
        USDA/USFS

"""
import xeofs as xe
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

from matplotlib.patheffects import withStroke
from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from dateutil import tz
from firewxpy.calc import scaling, Thermodynamics, unit_conversion
from firewxpy.utilities import file_functions
from metpy.units import units
from firewxpy.data_access import model_data
from cartopy.util import add_cyclic_point

mpl.rcParams['font.weight'] = 'bold'
local_time, utc_time = standard.plot_creation_time()

datacrs = ccrs.PlateCarree()

provinces = cfeature.NaturalEarthFeature(category='cultural', 
    name='admin_1_states_provinces_lines', scale='50m', facecolor='none', edgecolor='k')

props = dict(boxstyle='round', facecolor='wheat', alpha=1)

class ensemble_5_day_mean_eofs:

    r'''
    This class hosts 8-Day stats graphics for forecast ensemble data. 

    This includes the following: 

    1) Period Mean
    2) EOF1
    3) EOF2
    4) EOF1 Scores
    5) EOF2 Scores
    '''

    def plot_geopotential_height(model, hemisphere, level=500, data=False, ds=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

        r'''
        This function plots the following 8-Day Statistics over a period of 16-Days:

        1) Mean 500MB Geopotential Height
        2) EOF1 Geopotential Height
        3) EOF2 Geopotential Height
        4) EOF1 Scores Geopotential Height
        5) EOF2 Scores Geopotential Height

        Required Arguments: 
        
        1) model (String) - This is the model the user must select. 
                               
           Here are the choices: 
           1) GEFS0p50 - GEFS 0.5x0.5 degree
           2) CMCENS - Canadian Ensemble

        2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                             To look at any state use the 2-letter abbreviation for the state in either all capitals
                             or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                             CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                             North America use either: NA, na, North America or north america. If the user wishes to use custom
                             boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                             the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                             'oscc' for South Ops. 

        Optional Arguments: 
        
        1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
                             500 means 500mb or 500hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

        2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                            and passing the data in or if the function needs to download the data. A value of False means the data
                            is downloaded inside of the function while a value of True means the user is downloading the data outside
                            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                            things, it is recommended to set this value to True and download the data outside of the function and pass
                            it in so that the amount of data requests on the host servers can be minimized. 

        3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                        in the dataset. If the user wishes to download the data inside of the function, this value is None. 

        4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                     

        7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

        8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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
                               

        10) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        11) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        12) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        13) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        14) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        15) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        16) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

        18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

        19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

        20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

        21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

        22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

        23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

        24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

        25) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        26) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        27) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        28) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        29) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        30) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        31) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'.    

        32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                          This is a feature of matplotlib, as per their definition, the shrink is:
                                          "Fraction by which to multiply the size of the colorbar." 
                                          This should only be changed if the user wishes to make a custom plot. 
                                          Preset values are called from the settings module for each region. 

        39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                 Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                 when making a custom plot. 

        40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

        41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

        43) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

        44) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


        Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

        '''
    
        data=data
        level=level
        ds=ds
        show_rivers=show_rivers
        reference_system=reference_system
        state_border_linewidth=state_border_linewidth
        county_border_linewidth=county_border_linewidth
        gacc_border_linewidth=gacc_border_linewidth
        psa_border_linewidth=psa_border_linewidth 
        cwa_border_linewidth=cwa_border_linewidth
        nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
        nws_public_zones_linewidth=nws_public_zones_linewidth 
        state_border_linestyle=state_border_linestyle
        county_border_linestyle=county_border_linestyle
        gacc_border_linestyle=gacc_border_linestyle
        psa_border_linestyle=psa_border_linestyle 
        cwa_border_linestyle=cwa_border_linestyle
        nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
        nws_public_zones_linestyle=nws_public_zones_linestyle
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")
        
        shrink = 0.8
    
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
    
        str_level = f"{level} MB"
        
        
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 10
            step = 1
    
            if level == 850:
                level_idx = 2
            if level == 700:
                level_idx = 3
            if level == 500:
                level_idx = 4
            if level == 300:
                level_idx = 6
            if level == 250:
                level_idx = 7
            if level == 200:
                level_idx = 8
            
        if model == 'GFS0p25' or model == 'GFS0p25_1h':
            decimate = 10
            step = 2
            
            if level == 850:
                level_idx = 5
            if level == 700:
                level_idx = 8
            if level == 500:
                level_idx = 12
            if level == 300:
                level_idx = 16
            if level == 250:
                level_idx = 17
            if level == 200:
                level_idx = 18
            
        if model == 'GFS0p50':
            decimate = 10
            step = 2
            
            if level == 850:
                level_idx = 6
            if level == 700:
                level_idx = 12
            if level == 500:
                level_idx = 20
            if level == 300:
                level_idx = 28
            if level == 250:
                level_idx = 30
            if level == 200:
                level_idx = 32
        
        if model == 'GFS1p00':
            decimate = 10
            step = 2
    
            if level == 850:
                level_idx = 5
            if level == 700:
                level_idx = 8
            if level == 500:
                level_idx = 12
            if level == 300:
                level_idx = 16
            if level == 250:
                level_idx = 17
            if level == 200:
                level_idx = 18
    
        if hemisphere == 'N':
            mapcrs = ccrs.NorthPolarStereo()
            region ='custom'
            region_name = 'NORTHERN HEMISPHERE'
            wb = 360
            eb = 0
            sb = 25
            nb = 90

        if hemisphere == 'S':
            mapcrs = ccrs.SouthPolarStereo()
            region ='custom'
            region_name = 'SOUTHERN HEMISPHERE'
            wb = 360
            eb = 0
            sb = -25
            nb = -90
        
        if data == False:
            ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
            
        if data == True:
            ds = ds
    
        cmap = colormaps.gph_colormap()

        end = len(ds['time']) - 1
        ds1 = ds.sel(ens=ds['ens'][0], time=ds['time'][0:33])
        ds2 = ds.sel(ens=ds['ens'][0], time=ds['time'][32:65])
        time_1 = ds1['time']
        times_1 = time_1.to_pandas()
        time_2 = ds2['time']
        times_2 = time_2.to_pandas() 

        model_1 = xe.single.EOF(use_coslat=True)
        model_1.fit(ds1['hgtprs'], dim="time")
        model_1.explained_variance_ratio()
        components_1 = model_1.components()
        scores_1 = model_1.scores()
        avg_1 = ds1['hgtprs'].mean(dim='time')

        model_2 = xe.single.EOF(use_coslat=True)
        model_2.fit(ds2['hgtprs'], dim="time")
        model_2.explained_variance_ratio()
        components_2 = model_2.components()
        scores_2 = model_2.scores()
        avg_2 = ds2['hgtprs'].mean(dim='time')

        avg_1_lon = avg_1['lon']
        avg_1_lon_idx = avg_1.dims.index('lon')
        cyclic_avg_1, cyclic_avg_lon_1 = add_cyclic_point(avg_1.values, coord=avg_1_lon, axis=avg_1_lon_idx)

        avg_2_lon = avg_2['lon']
        avg_2_lon_idx = avg_2.dims.index('lon')
        cyclic_avg_2, cyclic_avg_lon_2 = add_cyclic_point(avg_2.values, coord=avg_2_lon, axis=avg_2_lon_idx)

        eofs_1_lon = components_1['lon']
        eofs_1_lon_idx = components_1.dims.index('lon')
        cyclic_eof_1, cyclic_eof_lon_1 = add_cyclic_point(components_1, coord=eofs_1_lon, axis=eofs_1_lon_idx)

        eofs_2_lon = components_2['lon']
        eofs_2_lon_idx = components_2.dims.index('lon')
        cyclic_eof_2, cyclic_eof_lon_2 = add_cyclic_point(components_2, coord=eofs_2_lon, axis=eofs_2_lon_idx)

        eof_levels_1_1 = np.arange(np.nanmin(components_1[0, level_idx, :, :]), (np.nanmax(components_1[0, level_idx, :, :]) + 0.00005), 0.00005)
        eof_levels_1_2 = np.arange(np.nanmin(components_2[0, level_idx, :, :]), (np.nanmax(components_2[0, level_idx, :, :]) + 0.00005), 0.00005)

        eof_levels_2_1 = np.arange(np.nanmin(components_1[1, level_idx, :, :]), (np.nanmax(components_1[1, level_idx, :, :]) + 0.00005), 0.00005)
        eof_levels_2_2 = np.arange(np.nanmin(components_2[1, level_idx, :, :]), (np.nanmax(components_2[1, level_idx, :, :]) + 0.00005), 0.00005)
        
        avg_1_levels = np.arange(int(round((np.nanmin(avg_1[level_idx, :, :])/10),0)), (int(round((np.nanmax(avg_1[level_idx, :, :])/10),0)) + 1), 1)
        ticks_1 = avg_1_levels[::3]
        avg_2_levels = np.arange(int(round(np.nanmin((avg_2[level_idx, :, :])/10),0)), (int(round((np.nanmax(avg_2[level_idx, :, :])/10),0)) + 1), 1)
        ticks_2 = avg_2_levels[::3]
    
        path1, path2, path3, path4, path5 = file_functions.forecast_model_eofs_paths(model, region_name, reference_system, 'Geopotential Height', str_level)
    
        for file in os.listdir(f"{path1}"):
            try:
                os.remove(f"{path1}/{file}")
            except Exception as e:
                pass

        for file in os.listdir(f"{path2}"):
            try:
                os.remove(f"{path2}/{file}")
            except Exception as e:
                pass

        for file in os.listdir(f"{path3}"):
            try:
                os.remove(f"{path3}/{file}")
            except Exception as e:
                pass

        for file in os.listdir(f"{path4}"):
            try:
                os.remove(f"{path4}/{file}")
            except Exception as e:
                pass

        for file in os.listdir(f"{path5}"):
            try:
                os.remove(f"{path5}/{file}")
            except Exception as e:
                pass
        
        for i in range(0, 2):
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)

            if i == 0:
                fname = f"PERIOD 1 AVG.png"
                plt.title("Valid: " +times_1.iloc[0].strftime('%a %d/%H UTC')+" - "+times_1.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                plt.title(f"{model.upper()} 8-DAY MEAN {str_level} GEOPOTENTIAL HEIGHT [DM]", fontsize=9, fontweight='bold', loc='left')
                cs = ax.contourf(cyclic_avg_lon_1, avg_1['lat'], (cyclic_avg_1[level_idx, :, :]/10), cmap=colormaps.gph_colormap(), levels=avg_1_levels, transform=datacrs, extend='both')
                c = ax.contour(cyclic_avg_lon_1, avg_1['lat'], (cyclic_avg_1[level_idx, :, :]/10), levels=avg_1_levels[::3], transform=datacrs, colors='black')
                ax.clabel(c, levels=avg_1_levels[::3], inline=True, fontsize=8, rightside_up=True)
                cbar = cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_1)
                fig.savefig(f"{path1}/{fname}", bbox_inches='tight')
                plt.close(fig)
                
            if i == 1:
                fname = f"PERIOD 2 AVG.png"
                plt.title("Valid: " +times_2.iloc[0].strftime('%a %d/%H UTC')+" - "+times_2.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                plt.title(f"{model.upper()} 8-DAY MEAN {str_level} GEOPOTENTIAL HEIGHT [DM]", fontsize=9, fontweight='bold', loc='left')
                cs = ax.contourf(cyclic_avg_lon_2, avg_2['lat'], (cyclic_avg_2[level_idx, :, :]/10), cmap=colormaps.gph_colormap(), levels=avg_2_levels, transform=datacrs, extend='both')
                c = ax.contour(cyclic_avg_lon_2, avg_2['lat'], (cyclic_avg_2[level_idx, :, :]/10), levels=avg_2_levels[::3], transform=datacrs, colors='black')
                ax.clabel(c, levels=avg_2_levels[::3], inline=True, fontsize=8, rightside_up=True)
                cbar = cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_2)
                fig.savefig(f"{path1}/{fname}", bbox_inches='tight')
                plt.close(fig)

                print(f"Saved Averages to f:{path1}")
            
            if mapcrs == datacrs:
                tim.sleep(10)

    
        for i in range(0, 2):
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)

            if i == 0:
                fname = f"PERIOD 1 EOF1.png"
                plt.title("Valid: " +times_1.iloc[0].strftime('%a %d/%H UTC')+" - "+times_1.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                plt.title(f"{model.upper()} EOF1 {str_level} 8-DAY GEOPOTENTIAL HEIGHT", fontsize=9, fontweight='bold', loc='left')
                ax.contourf(cyclic_eof_lon_1, components_1['lat'], cyclic_eof_1[0, level_idx, :, :], levels=eof_levels_1_1, cmap=colormaps.eof_colormap(), transform=datacrs, extend='both')
                fig.savefig(f"{path2}/{fname}", bbox_inches='tight')
                plt.close(fig)
 
            if i == 1:
                fname = f"PERIOD 2 EOF1.png"
                plt.title("Valid: " +times_2.iloc[0].strftime('%a %d/%H UTC')+" - "+times_2.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                plt.title(f"{model.upper()} EOF1 {str_level} 8-DAY GEOPOTENTIAL HEIGHT", fontsize=9, fontweight='bold', loc='left')
                ax.contourf(cyclic_eof_lon_2, components_2['lat'], cyclic_eof_2[0, level_idx, :, :], levels=eof_levels_1_2, cmap=colormaps.eof_colormap(), transform=datacrs, extend='both')
                fig.savefig(f"{path2}/{fname}", bbox_inches='tight')
                plt.close(fig)

                print(f"Saved Averages to f:{path2}")
            
            if mapcrs == datacrs:
                tim.sleep(10)     

        for i in range(0, 2):
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass

            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)

            if i == 0:
                fname = f"PERIOD 1 EOF2.png"
                plt.title("Valid: " +times_1.iloc[0].strftime('%a %d/%H UTC')+" - "+times_1.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                plt.title(f"{model.upper()} EOF2 {str_level} 8-DAY GEOPOTENTIAL HEIGHT", fontsize=9, fontweight='bold', loc='left')
                ax.contourf(cyclic_eof_lon_1, components_1['lat'], cyclic_eof_1[1, level_idx, :, :], levels=eof_levels_2_1, cmap=colormaps.eof_colormap(), transform=datacrs, extend='both')
                fig.savefig(f"{path3}/{fname}", bbox_inches='tight')
                plt.close(fig)
 
            if i == 1:
                fname = f"PERIOD 2 EOF2.png"
                plt.title("Valid: " +times_2.iloc[0].strftime('%a %d/%H UTC')+" - "+times_2.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                plt.title(f"{model.upper()} EOF2 {str_level} 8-DAY GEOPOTENTIAL HEIGHT", fontsize=9, fontweight='bold', loc='left')
                ax.contourf(cyclic_eof_lon_2, components_2['lat'], cyclic_eof_2[1, level_idx, :, :], levels=eof_levels_2_2, cmap=colormaps.eof_colormap(), transform=datacrs, extend='both')
                fig.savefig(f"{path3}/{fname}", bbox_inches='tight')
                plt.close(fig)

                print(f"Saved Averages to f:{path3}")
            
            if mapcrs == datacrs:
                tim.sleep(10)  


        for i in range(0, 2):
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1)
            ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
            ax.text(x1, -0.05, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax.text(x2, -0.05, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)

            if i == 0:
                fname = f"PERIOD 1 EOF1 SCORES.png"
                plt.title("Valid: " +times_1.iloc[0].strftime('%a %d/%H UTC')+" - "+times_1.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                plt.title(f"{model.upper()} EOF1 SCORES {str_level} 8-DAY GEOPOTENTIAL HEIGHT", fontsize=9, fontweight='bold', loc='left')
                ax.plot(scores_1['time'], scores_1[0, :], color='black')
                ax.fill_between(scores_1['time'], 0, scores_1[0, :], color='red', where=(scores_1[0, :] > 0), alpha=0.3)
                ax.fill_between(scores_1['time'], scores_1[0, :], 0, color='blue', where=(scores_1[0, :] < 0), alpha=0.3)
                fig.savefig(f"{path4}/{fname}", bbox_inches='tight')
                plt.close(fig)
 
            if i == 1:
                fname = f"PERIOD 2 EOF1 SCORES.png"
                plt.title("Valid: " +times_2.iloc[0].strftime('%a %d/%H UTC')+" - "+times_2.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                plt.title(f"{model.upper()} EOF1 SCORES {str_level} 8-DAY GEOPOTENTIAL HEIGHT", fontsize=9, fontweight='bold', loc='left')
                ax.plot(scores_2['time'], scores_2[0, :], color='black')
                ax.fill_between(scores_2['time'], 0, scores_2[0, :], color='red', where=(scores_2[0, :] > 0), alpha=0.3)
                ax.fill_between(scores_2['time'], scores_2[0, :], 0, color='blue', where=(scores_2[0, :] < 0), alpha=0.3)
                fig.savefig(f"{path4}/{fname}", bbox_inches='tight')
                plt.close(fig)

                print(f"Saved Averages to f:{path4}")
            
            if mapcrs == datacrs:
                tim.sleep(10)   

        for i in range(0, 2):
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1)
            ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
            ax.text(x1, -0.05, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax.text(x2, -0.05, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)

            if i == 0:
                fname = f"PERIOD 1 EOF2 SCORES.png"
                plt.title("Valid: " +times_1.iloc[0].strftime('%a %d/%H UTC')+" - "+times_1.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                plt.title(f"{model.upper()} EOF2 SCORES {str_level} 8-DAY GEOPOTENTIAL HEIGHT", fontsize=9, fontweight='bold', loc='left')
                ax.plot(scores_1['time'], scores_1[1, :], color='black')
                ax.fill_between(scores_1['time'], 0, scores_1[1, :], color='red', where=(scores_1[1, :] > 0), alpha=0.3)
                ax.fill_between(scores_1['time'], scores_1[1, :], 0, color='blue', where=(scores_1[1, :] < 0), alpha=0.3)
                fig.savefig(f"{path5}/{fname}", bbox_inches='tight')
                plt.close(fig)
 
            if i == 1:
                fname = f"PERIOD 2 EOF2 SCORES.png"
                plt.title("Valid: " +times_2.iloc[0].strftime('%a %d/%H UTC')+" - "+times_2.iloc[-1].strftime('%a %d/%H UTC')+"\nInitialization: "+times_1.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                plt.title(f"{model.upper()} EOF2 SCORES {str_level} 8-DAY GEOPOTENTIAL HEIGHT", fontsize=9, fontweight='bold', loc='left')
                ax.plot(scores_2['time'], scores_2[1, :], color='black')
                ax.fill_between(scores_2['time'], 0, scores_2[1, :], color='red', where=(scores_2[1, :] > 0), alpha=0.3)
                ax.fill_between(scores_2['time'], scores_2[1, :], 0, color='blue', where=(scores_2[1, :] < 0), alpha=0.3)
                fig.savefig(f"{path5}/{fname}", bbox_inches='tight')
                plt.close(fig)

                print(f"Saved Averages to f:{path5}")
            
            if mapcrs == datacrs:
                tim.sleep(10)   


class dynamics:

    r'''
    This class hosts the graphics for the following: 1) Vorticity/Geopotential Height/Wind
                                                     2) Geopotential Height
                                                     3) 24-Hour Geopotential Height Change
                                                     4) Geopotential Height/Wind
                                                     5) 10-Meter Wind/MSLP

    '''


    def plot_vorticity_geopotential_height_wind(model, region, level=500, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

        r'''
        This function plots the Geopotential Height/Vorticity/Wind Forecast for a specific level. 

        Required Arguments: 
        
        1) model (String) - This is the model the user must select. 
                               
           Here are the choices: 
           1) GFS0p25 - GFS 0.25x0.25 degree
           2) GFS0p50 - GFS 0.5x0.5 degree
           3) GFS1p00 - GFS 1.0x1.0 degree
           4) GEFS0p50 - GEFS 0.5x0.5 degree
           5) CMCENS - Canadian Ensemble
           6) NAM - North American Model
           7) NA NAM - 32km North American Model - Full North America

        2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                             To look at any state use the 2-letter abbreviation for the state in either all capitals
                             or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                             CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                             North America use either: NA, na, North America or north america. If the user wishes to use custom
                             boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                             the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                             'oscc' for South Ops. 

        Optional Arguments: 
        
        1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
                             500 means 500mb or 500hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

        2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                            and passing the data in or if the function needs to download the data. A value of False means the data
                            is downloaded inside of the function while a value of True means the user is downloading the data outside
                            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                            things, it is recommended to set this value to True and download the data outside of the function and pass
                            it in so that the amount of data requests on the host servers can be minimized. 

        3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                        in the dataset. If the user wishes to download the data inside of the function, this value is None. 

        4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                     

        7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

        8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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
                               

        10) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        11) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        12) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        13) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        14) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        15) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        16) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

        18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

        19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

        20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

        21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

        22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

        23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

        24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

        25) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        26) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        27) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        28) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        29) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        30) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        31) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'.    

        32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                          This is a feature of matplotlib, as per their definition, the shrink is:
                                          "Fraction by which to multiply the size of the colorbar." 
                                          This should only be changed if the user wishes to make a custom plot. 
                                          Preset values are called from the settings module for each region. 

        39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                 Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                 when making a custom plot. 

        40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

        41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

        43) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

        44) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


        Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

        '''
    
        data=data
        level=level
        ds=ds
        western_bound=western_bound
        eastern_bound=eastern_bound 
        southern_bound=southern_bound
        northern_bound=northern_bound
        show_rivers=show_rivers
        reference_system=reference_system
        state_border_linewidth=state_border_linewidth
        county_border_linewidth=county_border_linewidth
        gacc_border_linewidth=gacc_border_linewidth
        psa_border_linewidth=psa_border_linewidth 
        cwa_border_linewidth=cwa_border_linewidth
        nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
        nws_public_zones_linewidth=nws_public_zones_linewidth 
        state_border_linestyle=state_border_linestyle
        county_border_linestyle=county_border_linestyle
        gacc_border_linestyle=gacc_border_linestyle
        psa_border_linestyle=psa_border_linestyle 
        cwa_border_linestyle=cwa_border_linestyle
        nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
        nws_public_zones_linestyle=nws_public_zones_linestyle
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            mapcrs = ccrs.LambertConformal()
        else:
            mapcrs = ccrs.PlateCarree()
    
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
    
        str_level = f"{level} MB"
    
        if level == 850:
            levels = np.arange(96, 180, 4)
        if level == 700:
            levels = np.arange(240, 340, 4)
        if level == 300:
            levels = np.arange(840, 1020, 10)
        if level == 250:
            levels = np.arange(900, 1140, 10)
        if level == 200:
            levels = np.arange(1000, 1280, 10)
        
    
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
            decimate = 20
            step = 1
            
            if level == 850:
                level_idx = 6
            if level == 700:
                level_idx = 12
            if level == 500:
                level_idx = 20
            if level == 300:
                level_idx = 28
            if level == 250:
                level_idx = 30
            if level == 200:
                level_idx = 32
        
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 10
            step = 1
    
            if level == 850:
                level_idx = 2
            if level == 700:
                level_idx = 3
            if level == 500:
                level_idx = 4
            if level == 300:
                level_idx = 6
            if level == 250:
                level_idx = 7
            if level == 200:
                level_idx = 8
            
        if model == 'GFS0p25' or model == 'GFS0p25_1h':
            decimate = 10
            step = 2
            
            if level == 850:
                level_idx = 5
            if level == 700:
                level_idx = 8
            if level == 500:
                level_idx = 12
            if level == 300:
                level_idx = 16
            if level == 250:
                level_idx = 17
            if level == 200:
                level_idx = 18
            
        if model == 'GFS0p50':
            decimate = 10
            step = 2
            
            if level == 850:
                level_idx = 6
            if level == 700:
                level_idx = 12
            if level == 500:
                level_idx = 20
            if level == 300:
                level_idx = 28
            if level == 250:
                level_idx = 30
            if level == 200:
                level_idx = 32
        
        if model == 'GFS1p00':
            decimate = 10
            step = 2
    
            if level == 850:
                level_idx = 5
            if level == 700:
                level_idx = 8
            if level == 500:
                level_idx = 12
            if level == 300:
                level_idx = 16
            if level == 250:
                level_idx = 17
            if level == 200:
                level_idx = 18
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
            wb=western_bound
            eb=eastern_bound
            sb=southern_bound
            nb=northern_bound
            x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
        else:
            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
            sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)
        
        if data == False:
            if model == 'RAP' or model == 'RAP 32':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
            else:
                ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
            
        if data == True:
            ds = ds
    
    
        if model == 'CMCENS' or model == 'GEFS0p50':
            ds['absvprs'] = mpcalc.vorticity((ds['ugrdprs'][0, :, level_idx, :, :] * units('m/s')), (ds['vgrdprs'][0, :, level_idx, :, :] * units('m/s')))

        if model == 'RAP' or model == 'RAP 32':
            ds['absvprs'] = mpcalc.vorticity((ds['ugrdprs'][:, level_idx, :, :] * units('m/s')), (ds['vgrdprs'][:, level_idx, :, :] * units('m/s')))
    
        cmap = colormaps.vorticity_colormap()
    
        end = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()
    
    
        path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, 'Height Vorticity Wind', str_level)
    
        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
        
        for t in range(0, end, step):
        
            fname = f"Image_{t}.png"
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            model = model.upper()
            plt.title(f"{model} {str_level} GPH [DM]/ABS VORT [1/S]/WIND [KTS]", fontsize=9, fontweight='bold', loc='left')
            plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
            
            lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
            
            stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                             transform=ccrs.PlateCarree(), zorder=3, fontsize=5, clip_on=True)
    
    
            if model == 'CMCENS' or model == 'GEFS0P50':
    
                stn.plot_barb((ds['ugrdprs'][0, t, level_idx, ::decimate, ::decimate] * 1.94384), (ds['vgrdprs'][0, t, level_idx, ::decimate, ::decimate] * 1.94384), color='black', alpha=1, zorder=3, linewidth=0.25)
    
                if level == 500:
                    c_neg = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=np.arange(440, 540, 4), colors='darkblue', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                    c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=[540], colors='black', zorder=2, transform=datacrs, linewidths=1)
                    c_pos = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=np.arange(544, 624, 4), colors='darkred', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                    ax.clabel(c_neg, levels=np.arange(440, 540, 4), inline=True, fontsize=8, rightside_up=True)
                    ax.clabel(c, levels=[540], inline=True, fontsize=8, rightside_up=True)
                    ax.clabel(c_pos, levels=np.arange(544, 624, 4), inline=True, fontsize=8, rightside_up=True)
    
                else:                
                    c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                    ax.clabel(c, levels=levels, inline=True, fontsize=8, rightside_up=True)
                    
                cs = ax.contourf(ds['lon'], ds['lat'], abs(ds['absvprs'][t, :, :]), cmap=cmap, transform=datacrs, levels=np.arange(0, 55e-5, 50e-6), alpha=0.35, extend='max')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', format="{x:.0e}")
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
    
    
            else:
                
                stn.plot_barb((ds['ugrdprs'][t, level_idx, ::decimate, ::decimate] * 1.94384), (ds['vgrdprs'][t, level_idx, ::decimate, ::decimate] * 1.94384), color='black', alpha=1, zorder=3, linewidth=0.25)
    
                if level == 500:
                    c_neg = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=np.arange(440, 540, 4), colors='darkblue', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                    c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=[540], colors='black', zorder=2, transform=datacrs, linewidths=1)
                    c_pos = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=np.arange(544, 624, 4), colors='darkred', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                    ax.clabel(c_neg, levels=np.arange(440, 540, 4), inline=True, fontsize=8, rightside_up=True)
                    ax.clabel(c, levels=[540], inline=True, fontsize=8, rightside_up=True)
                    ax.clabel(c_pos, levels=np.arange(544, 624, 4), inline=True, fontsize=8, rightside_up=True)
    
                else:
                    c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                    ax.clabel(c, levels=levels, inline=True, fontsize=8, rightside_up=True)
                try:
                    cs = ax.contourf(ds['lon'], ds['lat'], abs(ds['absvprs'][t, level_idx, :, :]), cmap=cmap, transform=datacrs, levels=np.arange(0, 55e-5, 50e-6), alpha=0.35, extend='max')
                except Exception as e:
                    cs = ax.contourf(ds['lon'], ds['lat'], abs(ds['absvprs'][t, :, :]), cmap=cmap, transform=datacrs, levels=np.arange(0, 55e-5, 50e-6), alpha=0.35, extend='max')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', format="{x:.0e}")
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
            
                if mapcrs == datacrs:
                    tim.sleep(10)
        print(f"Saved forecast graphics to {path_print}.")
    
    
    def plot_geopotential_height(model, region, level=500, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

        r'''
        This function plots the Geopotential Height Forecast for a specific level. 

        Required Arguments: 
        
        1) model (String) - This is the model the user must select. 
                               
           Here are the choices: 
           1) GFS0p25 - GFS 0.25x0.25 degree
           2) GFS0p50 - GFS 0.5x0.5 degree
           3) GFS1p00 - GFS 1.0x1.0 degree
           4) GEFS0p50 - GEFS 0.5x0.5 degree
           5) CMCENS - Canadian Ensemble
           6) NAM - North American Model
           7) NA NAM - 32km North American Model - Full North America

        2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                             To look at any state use the 2-letter abbreviation for the state in either all capitals
                             or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                             CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                             North America use either: NA, na, North America or north america. If the user wishes to use custom
                             boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                             the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                             'oscc' for South Ops. 

        Optional Arguments: 
        
        1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
                             500 means 500mb or 500hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

        2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                            and passing the data in or if the function needs to download the data. A value of False means the data
                            is downloaded inside of the function while a value of True means the user is downloading the data outside
                            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                            things, it is recommended to set this value to True and download the data outside of the function and pass
                            it in so that the amount of data requests on the host servers can be minimized. 

        3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                        in the dataset. If the user wishes to download the data inside of the function, this value is None. 

        4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                     

        7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

        8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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
                               

        10) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        11) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        12) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        13) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        14) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        15) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        16) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

        18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

        19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

        20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

        21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

        22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

        23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

        24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

        25) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        26) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        27) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        28) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        29) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        30) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        31) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'.    

        32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                          This is a feature of matplotlib, as per their definition, the shrink is:
                                          "Fraction by which to multiply the size of the colorbar." 
                                          This should only be changed if the user wishes to make a custom plot. 
                                          Preset values are called from the settings module for each region. 

        39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                 Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                 when making a custom plot. 

        40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

        41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

        43) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

        44) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


        Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

        '''
    
        data=data
        level=level
        ds=ds
        western_bound=western_bound
        eastern_bound=eastern_bound 
        southern_bound=southern_bound
        northern_bound=northern_bound
        show_rivers=show_rivers
        reference_system=reference_system
        state_border_linewidth=state_border_linewidth
        county_border_linewidth=county_border_linewidth
        gacc_border_linewidth=gacc_border_linewidth
        psa_border_linewidth=psa_border_linewidth 
        cwa_border_linewidth=cwa_border_linewidth
        nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
        nws_public_zones_linewidth=nws_public_zones_linewidth 
        state_border_linestyle=state_border_linestyle
        county_border_linestyle=county_border_linestyle
        gacc_border_linestyle=gacc_border_linestyle
        psa_border_linestyle=psa_border_linestyle 
        cwa_border_linestyle=cwa_border_linestyle
        nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
        nws_public_zones_linestyle=nws_public_zones_linestyle
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            mapcrs = ccrs.LambertConformal()
        else:
            mapcrs = ccrs.PlateCarree()
    
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
    
        str_level = f"{level} MB"
    
        if level == 850:
            levels = np.arange(96, 180, 4)
            ticks = levels[::2]
        if level == 700:
            levels = np.arange(240, 340, 4)
            ticks = levels[::2]
        if level == 500:
            levels = np.arange(480, 604, 4)
            ticks = levels[::2]
        if level == 300:
            levels = np.arange(840, 1020, 10)
            ticks = levels[::2]
        if level == 250:
            levels = np.arange(900, 1140, 10)
            ticks = levels[::2]
        if level == 200:
            levels = np.arange(1000, 1280, 10)
            ticks = levels[::2]
        
    
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
            decimate = 20
            step = 1
            
            if level == 850:
                level_idx = 6
            if level == 700:
                level_idx = 12
            if level == 500:
                level_idx = 20
            if level == 300:
                level_idx = 28
            if level == 250:
                level_idx = 30
            if level == 200:
                level_idx = 32
        
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 10
            step = 1
    
            if level == 850:
                level_idx = 2
            if level == 700:
                level_idx = 3
            if level == 500:
                level_idx = 4
            if level == 300:
                level_idx = 6
            if level == 250:
                level_idx = 7
            if level == 200:
                level_idx = 8
            
        if model == 'GFS0p25' or model == 'GFS0p25_1h':
            decimate = 10
            step = 2
            
            if level == 850:
                level_idx = 5
            if level == 700:
                level_idx = 8
            if level == 500:
                level_idx = 12
            if level == 300:
                level_idx = 16
            if level == 250:
                level_idx = 17
            if level == 200:
                level_idx = 18
            
        if model == 'GFS0p50':
            decimate = 10
            step = 2
            
            if level == 850:
                level_idx = 6
            if level == 700:
                level_idx = 12
            if level == 500:
                level_idx = 20
            if level == 300:
                level_idx = 28
            if level == 250:
                level_idx = 30
            if level == 200:
                level_idx = 32
        
        if model == 'GFS1p00':
            decimate = 10
            step = 2
    
            if level == 850:
                level_idx = 5
            if level == 700:
                level_idx = 8
            if level == 500:
                level_idx = 12
            if level == 300:
                level_idx = 16
            if level == 250:
                level_idx = 17
            if level == 200:
                level_idx = 18
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
            wb=western_bound
            eb=eastern_bound
            sb=southern_bound
            nb=northern_bound
            x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
        else:
            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
            sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)
        
        if data == False:
            if model == 'RAP' or model == 'RAP 32':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
            else:
                ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
            
        if data == True:
            ds = ds
    
        cmap = colormaps.gph_colormap()
    
        end = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()
    
    
        path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, 'Geopotential Height', str_level)
    
        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
        
        for t in range(0, end, step):
        
            fname = f"Image_{t}.png"
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            model = model.upper()
            plt.title(f"{model} {str_level} GEOPOTENTIAL HEIGHT [DM]", fontsize=9, fontweight='bold', loc='left')
            plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
    
    
            if model == 'CMCENS' or model == 'GEFS0P50':
                  
                c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                ax.clabel(c, levels=levels, inline=True, fontsize=8, rightside_up=True)
                    
                cs = ax.contourf(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)

                if mapcrs == datacrs:
                    tim.sleep(10)
    
    
            else:
                
                c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                ax.clabel(c, levels=levels, inline=True, fontsize=8, rightside_up=True)
                
                cs = ax.contourf(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
        print(f"Saved forecast graphics to {path_print}.")

    def plot_24hr_geopotential_height_change(model, region, level=500, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

        r'''
        This function plots the 24-Hour Gepotential Height Change Forecast for a specific level. 

        Required Arguments: 
        
        1) model (String) - This is the model the user must select. 
                               
           Here are the choices: 
           1) GFS0p25 - GFS 0.25x0.25 degree
           2) GFS0p50 - GFS 0.5x0.5 degree
           3) GFS1p00 - GFS 1.0x1.0 degree
           4) GEFS0p50 - GEFS 0.5x0.5 degree
           5) CMCENS - Canadian Ensemble
           6) NAM - North American Model
           7) NA NAM - 32km North American Model - Full North America
           
        2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                             To look at any state use the 2-letter abbreviation for the state in either all capitals
                             or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                             CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                             North America use either: NA, na, North America or north america. If the user wishes to use custom
                             boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                             the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                             'oscc' for South Ops. 

        Optional Arguments: 
        
        1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
                             500 means 500mb or 500hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

        2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                            and passing the data in or if the function needs to download the data. A value of False means the data
                            is downloaded inside of the function while a value of True means the user is downloading the data outside
                            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                            things, it is recommended to set this value to True and download the data outside of the function and pass
                            it in so that the amount of data requests on the host servers can be minimized. 

        3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                        in the dataset. If the user wishes to download the data inside of the function, this value is None. 

        4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                     

        7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

        8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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
                               

        10) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        11) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        12) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        13) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        14) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        15) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        16) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

        18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

        19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

        20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

        21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

        22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

        23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

        24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

        25) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        26) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        27) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        28) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        29) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        30) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        31) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'.    

        32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                          This is a feature of matplotlib, as per their definition, the shrink is:
                                          "Fraction by which to multiply the size of the colorbar." 
                                          This should only be changed if the user wishes to make a custom plot. 
                                          Preset values are called from the settings module for each region. 

        39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                 Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                 when making a custom plot. 

        40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

        41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

        43) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

        44) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


        Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

        '''
    
        data=data
        level=level
        ds=ds
        western_bound=western_bound
        eastern_bound=eastern_bound 
        southern_bound=southern_bound
        northern_bound=northern_bound
        show_rivers=show_rivers
        reference_system=reference_system
        state_border_linewidth=state_border_linewidth
        county_border_linewidth=county_border_linewidth
        gacc_border_linewidth=gacc_border_linewidth
        psa_border_linewidth=psa_border_linewidth 
        cwa_border_linewidth=cwa_border_linewidth
        nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
        nws_public_zones_linewidth=nws_public_zones_linewidth 
        state_border_linestyle=state_border_linestyle
        county_border_linestyle=county_border_linestyle
        gacc_border_linestyle=gacc_border_linestyle
        psa_border_linestyle=psa_border_linestyle 
        cwa_border_linestyle=cwa_border_linestyle
        nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
        nws_public_zones_linestyle=nws_public_zones_linestyle
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            mapcrs = ccrs.LambertConformal()
        else:
            mapcrs = ccrs.PlateCarree()
    
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
    
        str_level = f"{level} MB"
    
        levels = np.arange(-30, 31, 1)
        ticks = levels[::5]
    
        negative = np.arange(-30, 5, 5)
        positive = np.arange(5, 35, 5)
        
        
        if model == 'CMCENS' or model == 'GEFS0p50':
            increment = 4
            step = 1
    
            if level == 850:
                level_idx = 2
            if level == 700:
                level_idx = 3
            if level == 500:
                level_idx = 4
            if level == 300:
                level_idx = 6
            if level == 250:
                level_idx = 7
            if level == 200:
                level_idx = 8
            
        if model == 'GFS0p25' or model == 'GFS0p25_1h':
            step = 2
            increment = 8
            
            if level == 850:
                level_idx = 5
            if level == 700:
                level_idx = 8
            if level == 500:
                level_idx = 12
            if level == 300:
                level_idx = 16
            if level == 250:
                level_idx = 17
            if level == 200:
                level_idx = 18
            
        if model == 'GFS0p50':
            step = 2
            increment = 8
            
            if level == 850:
                level_idx = 6
            if level == 700:
                level_idx = 12
            if level == 500:
                level_idx = 20
            if level == 300:
                level_idx = 28
            if level == 250:
                level_idx = 30
            if level == 200:
                level_idx = 32
        
        if model == 'GFS1p00':
            step = 2
            increment = 8
            
            if level == 850:
                level_idx = 5
            if level == 700:
                level_idx = 8
            if level == 500:
                level_idx = 12
            if level == 300:
                level_idx = 16
            if level == 250:
                level_idx = 17
            if level == 200:
                level_idx = 18
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
            wb=western_bound
            eb=eastern_bound
            sb=southern_bound
            nb=northern_bound
            x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
        else:
            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
            sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)
        
        if data == False:
            if model == 'RAP' or model == 'RAP 32':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
            else:
                ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
            
        if data == True:
            ds = ds
    
        cmap = colormaps.gph_change_colormap()
    
        end = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()
    
    
        path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, '24-Hour Geopotential Height Change', str_level)
    
        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
        
        for t in range(0, end, step):
    
            t1 = t + increment
        
            fname = f"Image_{t}.png"
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            model = model.upper()
            plt.title(f"{model} {str_level} 24-HR GEOPOTENTIAL HEIGHT CHANGE [ΔDM]", fontsize=9, fontweight='bold', loc='left')
            try:
                plt.title("Forecast Valid: " +times.iloc[t1].strftime('%a %d/%H UTC')+" - "+times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            except Exception as e:
                pass
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
    
    
            if model == 'CMCENS' or model == 'GEFS0P50':
    
                try:
    
                    c_low = ax.contour(ds['lon'], ds['lat'], ((ds['hgtprs'][0, t1, level_idx, :, :] - ds['hgtprs'][0, t, level_idx, :, :])/10), levels=negative, colors='blue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c_low, levels=negative, inline=True, fontsize=8, rightside_up=True)
        
                    c = ax.contour(ds['lon'], ds['lat'], ((ds['hgtprs'][0, t1, level_idx, :, :] - ds['hgtprs'][0, t, level_idx, :, :])/10), levels=[0], colors='black', zorder=2, transform=datacrs, linewidths=1, linestyles='-')
                    ax.clabel(c, levels=[0], inline=True, fontsize=8, rightside_up=True)
        
                    c_high = ax.contour(ds['lon'], ds['lat'], ((ds['hgtprs'][0, t1, level_idx, :, :] - ds['hgtprs'][0, t, level_idx, :, :])/10), levels=positive, colors='red', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c_high, levels=positive, inline=True, fontsize=8, rightside_up=True)
                        
                    cs = ax.contourf(ds['lon'], ds['lat'], ((ds['hgtprs'][0, t1, level_idx, :, :] - ds['hgtprs'][0, t, level_idx, :, :])/10), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
        
                    fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                    plt.close(fig)
                    if mapcrs == datacrs:
                        tim.sleep(10)
    
                except Exception as e:
                    pass
    
    
            else:
    
                try:
                    c_low = ax.contour(ds['lon'], ds['lat'], ((ds['hgtprs'][t1, level_idx, :, :] - ds['hgtprs'][t, level_idx, :, :])/10), levels=negative, colors='blue', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c_low, levels=negative, inline=True, fontsize=8, rightside_up=True)
        
                    c_high = ax.contour(ds['lon'], ds['lat'], ((ds['hgtprs'][t1, level_idx, :, :] - ds['hgtprs'][t, level_idx, :, :])/10), levels=positive, colors='red', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c_high, levels=positive, inline=True, fontsize=8, rightside_up=True)
        
                    c = ax.contour(ds['lon'], ds['lat'], ((ds['hgtprs'][t1, level_idx, :, :] - ds['hgtprs'][t, level_idx, :, :])/10), levels=[0], colors='black', zorder=2, transform=datacrs, linewidths=1, linestyles='-')
                    ax.clabel(c, levels=[0], inline=True, fontsize=8, rightside_up=True)
                    
                    cs = ax.contourf(ds['lon'], ds['lat'], ((ds['hgtprs'][t1, level_idx, :, :] - ds['hgtprs'][t, level_idx, :, :])/10), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
            
                    fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                    plt.close(fig)
                    if mapcrs == datacrs:
                        tim.sleep(10)
                except Exception as e:
                    pass
        print(f"Saved forecast graphics to {path_print}.")

    def plot_geopotential_height_and_wind(model, region, level=250, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

        r'''
        This function plots the Geopotential Height/Wind Forecast for a specific level. 

        Required Arguments: 
        
        1) model (String) - This is the model the user must select. 
                               
           Here are the choices: 
           1) GFS0p25 - GFS 0.25x0.25 degree
           2) GFS0p50 - GFS 0.5x0.5 degree
           3) GFS1p00 - GFS 1.0x1.0 degree
           4) GEFS0p50 - GEFS 0.5x0.5 degree
           5) CMCENS - Canadian Ensemble
           6) NAM - North American Model
           7) NA NAM - 32km North American Model - Full North America

    2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                         To look at any state use the 2-letter abbreviation for the state in either all capitals
                         or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                         CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                         North America use either: NA, na, North America or north america. If the user wishes to use custom
                         boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                         the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                         'oscc' for South Ops. 

        Optional Arguments: 
        
        1) level (Integer) - Default = 500. This is the level in millibars or hectopascals at which the user wishes to examine. 
                             500 means 500mb or 500hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

        2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                            and passing the data in or if the function needs to download the data. A value of False means the data
                            is downloaded inside of the function while a value of True means the user is downloading the data outside
                            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                            things, it is recommended to set this value to True and download the data outside of the function and pass
                            it in so that the amount of data requests on the host servers can be minimized. 

        3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                        in the dataset. If the user wishes to download the data inside of the function, this value is None. 

        4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                     

        7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

        8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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
                               

        10) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        11) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        12) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        13) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        14) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        15) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        16) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

        18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

        19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

        20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

        21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

        22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

        23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

        24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

        25) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        26) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        27) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        28) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        29) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        30) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        31) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'.    

        32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                          This is a feature of matplotlib, as per their definition, the shrink is:
                                          "Fraction by which to multiply the size of the colorbar." 
                                          This should only be changed if the user wishes to make a custom plot. 
                                          Preset values are called from the settings module for each region. 

        39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                 Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                 when making a custom plot. 

        40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

        41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

        43) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

        44) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


        Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

        '''
    
        data=data
        level=level
        ds=ds
        western_bound=western_bound
        eastern_bound=eastern_bound 
        southern_bound=southern_bound
        northern_bound=northern_bound
        show_rivers=show_rivers
        reference_system=reference_system
        state_border_linewidth=state_border_linewidth
        county_border_linewidth=county_border_linewidth
        gacc_border_linewidth=gacc_border_linewidth
        psa_border_linewidth=psa_border_linewidth 
        cwa_border_linewidth=cwa_border_linewidth
        nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
        nws_public_zones_linewidth=nws_public_zones_linewidth 
        state_border_linestyle=state_border_linestyle
        county_border_linestyle=county_border_linestyle
        gacc_border_linestyle=gacc_border_linestyle
        psa_border_linestyle=psa_border_linestyle 
        cwa_border_linestyle=cwa_border_linestyle
        nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
        nws_public_zones_linestyle=nws_public_zones_linestyle
        x1=x1 
        y1=y1
        x2=x2
        y2=y2 
        x3=x3
        y3=y3 
        shrink=shrink
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            mapcrs = ccrs.LambertConformal()
        else:
            mapcrs = ccrs.PlateCarree()
    
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
    
            str_level = f"{level} MB"
        
            if level == 850:
                levels = np.arange(96, 180, 4)
                speeds = np.arange(20, 101, 1)
                ticks = speeds[::5]
            if level == 700:
                levels = np.arange(240, 340, 4)
                speeds = np.arange(20, 101, 1)
                ticks = speeds[::5]
            if level == 500:
                speeds = np.arange(40, 121, 1)
                ticks = speeds[::5]
            if level == 300:
                levels = np.arange(840, 1020, 10)
                speeds = np.arange(80, 161, 1)
                ticks = speeds[::5]
            if level == 250:
                levels = np.arange(900, 1140, 10)
                speeds = np.arange(80, 161, 1)
                ticks = speeds[::5]
            if level == 200:
                levels = np.arange(1000, 1280, 10)
                speeds = np.arange(80, 161, 1)
                ticks = speeds[::5]
            
        
            if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
                decimate = 20
                step = 1
                
                if level == 850:
                    level_idx = 6
                if level == 700:
                    level_idx = 12
                if level == 500:
                    level_idx = 20
                if level == 300:
                    level_idx = 28
                if level == 250:
                    level_idx = 30
                if level == 200:
                    level_idx = 32
            
            if model == 'CMCENS' or model == 'GEFS0p50':
                decimate = 10
                step = 1
        
                if level == 850:
                    level_idx = 2
                if level == 700:
                    level_idx = 3
                if level == 500:
                    level_idx = 4
                if level == 300:
                    level_idx = 6
                if level == 250:
                    level_idx = 7
                if level == 200:
                    level_idx = 8
                
            if model == 'GFS0p25' or model == 'GFS0p25_1h':
                decimate = 10
                step = 2
                
                if level == 850:
                    level_idx = 5
                if level == 700:
                    level_idx = 8
                if level == 500:
                    level_idx = 12
                if level == 300:
                    level_idx = 16
                if level == 250:
                    level_idx = 17
                if level == 200:
                    level_idx = 18
                
            if model == 'GFS0p50':
                decimate = 10
                step = 2
                
                if level == 850:
                    level_idx = 6
                if level == 700:
                    level_idx = 12
                if level == 500:
                    level_idx = 20
                if level == 300:
                    level_idx = 28
                if level == 250:
                    level_idx = 30
                if level == 200:
                    level_idx = 32
            
            if model == 'GFS1p00':
                decimate = 10
                step = 2
        
                if level == 850:
                    level_idx = 5
                if level == 700:
                    level_idx = 8
                if level == 500:
                    level_idx = 12
                if level == 300:
                    level_idx = 16
                if level == 250:
                    level_idx = 17
                if level == 200:
                    level_idx = 18
    
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
            wb=western_bound
            eb=eastern_bound
            sb=southern_bound
            nb=northern_bound
            x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
        else:
            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
            sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)
        
        if data == False:
            if model == 'RAP' or model == 'RAP 32':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
            else:
                ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
            
        if data == True:
            ds = ds
    
        cmap = colormaps.wind_speed_colormap()
    
        end = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()
    
    
        path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, 'Geopotential Height & Wind', str_level)
    
        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
        
        for t in range(0, end, step):
        
            fname = f"Image_{t}.png"
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            model = model.upper()
            plt.title(f"{model} {str_level} GEOPOTENTIAL HEIGHT [DM] & WIND [KTS]", fontsize=9, fontweight='bold', loc='left')
            plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
            
            lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
            
            stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                             transform=ccrs.PlateCarree(), zorder=3, fontsize=6, clip_on=True)
    
    
            if model == 'CMCENS' or model == 'GEFS0P50':
        
                stn.plot_barb((ds['ugrdprs'][0, t, level_idx, ::decimate, ::decimate] * 1.94384), (ds['vgrdprs'][0, t, level_idx, ::decimate, ::decimate] * 1.94384), color='black', alpha=1, zorder=3, linewidth=0.25)
    
                if level == 500:
                    c_neg = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=np.arange(440, 540, 4), colors='darkblue', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                    c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=[540], colors='black', zorder=2, transform=datacrs, linewidths=1)
                    c_pos = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=np.arange(544, 624, 4), colors='darkred', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                    ax.clabel(c_neg, levels=np.arange(440, 540, 4), inline=True, fontsize=8, rightside_up=True)
                    ax.clabel(c, levels=[540], inline=True, fontsize=8, rightside_up=True)
                    ax.clabel(c_pos, levels=np.arange(544, 624, 4), inline=True, fontsize=8, rightside_up=True)
    
                else:                
                    c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                    ax.clabel(c, levels=levels, inline=True, fontsize=8, rightside_up=True)
                    
                cs = ax.contourf(ds['lon'], ds['lat'], (mpcalc.wind_speed((ds['ugrdprs'][0, t, level_idx, :, :] *units('m/s')), (ds['vgrdprs'][0, t, level_idx, :, :] *units('m/s'))) * 1.94384), cmap=cmap, transform=datacrs, levels=speeds, alpha=0.35, extend='max')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
    
    
            else:
                
                stn.plot_barb((ds['ugrdprs'][t, level_idx, ::decimate, ::decimate] * 1.94384), (ds['vgrdprs'][t, level_idx, ::decimate, ::decimate] * 1.94384), color='black', alpha=1, zorder=3, linewidth=0.25)
    
                if level == 500:
                    c_neg = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=np.arange(440, 540, 4), colors='darkblue', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                    c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=[540], colors='black', zorder=2, transform=datacrs, linewidths=1)
                    c_pos = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=np.arange(544, 624, 4), colors='darkred', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                    ax.clabel(c_neg, levels=np.arange(440, 540, 4), inline=True, fontsize=8, rightside_up=True)
                    ax.clabel(c, levels=[540], inline=True, fontsize=8, rightside_up=True)
                    ax.clabel(c_pos, levels=np.arange(544, 624, 4), inline=True, fontsize=8, rightside_up=True)
    
                else:
                    c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                    ax.clabel(c, levels=levels, inline=True, fontsize=8, rightside_up=True)
                
                cs = ax.contourf(ds['lon'], ds['lat'], (mpcalc.wind_speed((ds['ugrdprs'][t, level_idx, :, :] *units('m/s')), (ds['vgrdprs'][t, level_idx, :, :] *units('m/s'))) * 1.94384), cmap=cmap, transform=datacrs, levels=speeds, alpha=0.35, extend='max')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
        print(f"Saved forecast graphics to {path_print}.")

    def plot_10m_winds_mslp(model, region, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

        r'''
        This function plots the 10-Meter Wind/MSLP Forecast. 

        Required Arguments: 
        
        1) model (String) - This is the model the user must select. 
                               
           Here are the choices: 
           1) GFS0p25 - GFS 0.25x0.25 degree
           2) GFS0p50 - GFS 0.5x0.5 degree
           3) GFS1p00 - GFS 1.0x1.0 degree
           4) GEFS0p50 - GEFS 0.5x0.5 degree
           5) CMCENS - Canadian Ensemble
           6) NAM - North American Model
           7) NA NAM - 32km North American Model - Full North America
           8) RAP - Rapid Refresh Model
           9) RAP 32 - 32km Rapid Refresh Model - Full North America

        2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                             To look at any state use the 2-letter abbreviation for the state in either all capitals
                             or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                             CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                             North America use either: NA, na, North America or north america. If the user wishes to use custom
                             boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                             the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                             'oscc' for South Ops. 

        Optional Arguments: 
        
        1) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                            and passing the data in or if the function needs to download the data. A value of False means the data
                            is downloaded inside of the function while a value of True means the user is downloading the data outside
                            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                            things, it is recommended to set this value to True and download the data outside of the function and pass
                            it in so that the amount of data requests on the host servers can be minimized. 

        2) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                        in the dataset. If the user wishes to download the data inside of the function, this value is None. 

        3) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        4) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        5) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                     

        6) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

        7) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        8) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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

        31) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        32) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        33) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        34) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        35) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        36) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        37) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                          This is a feature of matplotlib, as per their definition, the shrink is:
                                          "Fraction by which to multiply the size of the colorbar." 
                                          This should only be changed if the user wishes to make a custom plot. 
                                          Preset values are called from the settings module for each region. 

        38) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                 Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                 when making a custom plot. 

        39) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

        40) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        41) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

        42) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

        43) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


        Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

        '''
    
        data=data
        ds=ds
        western_bound=western_bound
        eastern_bound=eastern_bound 
        southern_bound=southern_bound
        northern_bound=northern_bound
        show_rivers=show_rivers
        reference_system=reference_system
        state_border_linewidth=state_border_linewidth
        county_border_linewidth=county_border_linewidth
        gacc_border_linewidth=gacc_border_linewidth
        psa_border_linewidth=psa_border_linewidth 
        cwa_border_linewidth=cwa_border_linewidth
        nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
        nws_public_zones_linewidth=nws_public_zones_linewidth 
        state_border_linestyle=state_border_linestyle
        county_border_linestyle=county_border_linestyle
        gacc_border_linestyle=gacc_border_linestyle
        psa_border_linestyle=psa_border_linestyle 
        cwa_border_linestyle=cwa_border_linestyle
        nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
        nws_public_zones_linestyle=nws_public_zones_linestyle
        x1=x1 
        y1=y1
        x2=x2
        y2=y2 
        x3=x3
        y3=y3 
        shrink=shrink
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            mapcrs = ccrs.LambertConformal()
        else:
            mapcrs = ccrs.PlateCarree()
    
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
    
        str_level = f"SURFACE"
    
        mslp_levels = np.arange(850, 1104, 4)
        speeds = np.arange(10, 81, 1)
        mslp_labels = mslp_levels
        speed_ticks = speeds[::5]
    
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
            step = 1
        
        if model == 'CMCENS' or model == 'GEFS0p50':
            step = 1
            
        if model == 'GFS0p25' or model == 'GFS0p25_1h':
            step = 2
            
        if model == 'GFS0p50':
            step = 2
        
        if model == 'GFS1p00':
            step = 2
    
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
            wb=western_bound
            eb=eastern_bound
            sb=southern_bound
            nb=northern_bound
            x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
        else:
            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
            sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)
        
        if data == False:
            if model == 'RAP' or model == 'RAP 32':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
            else:
                ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
            
        if data == True:
            ds = ds
    
        cmap = colormaps.cross_section_wind_speed()
    
        end = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()
    
    
        path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, '10m Wind & MSLP', str_level)
    
        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
        
        for t in range(0, end, step):
        
            fname = f"Image_{t}.png"
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            model = model.upper()
            plt.title(f"{model} MSLP [MB] & 10M WIND [MPH]", fontsize=9, fontweight='bold', loc='left')
            plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
            
            lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
            
            stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                             transform=ccrs.PlateCarree(), zorder=3, fontsize=6, clip_on=True)
    
    
            if model == 'CMCENS' or model == 'GEFS0P50':
    
                stn.plot_barb((ds['ugrd10m'][0, t, ::decimate, ::decimate] * 2.23694), (ds['vgrd10m'][0, t, ::decimate, ::decimate] * 2.23694), color='black', alpha=1, zorder=3, linewidth=0.5)
                   
                c = ax.contour(ds['lon'], ds['lat'], (ds['prmslmsl'][0, t, :, :]/100), levels=mslp_levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                ax.clabel(c, levels=mslp_levels, inline=True, fontsize=8, rightside_up=True)
                    
                cs = ax.contourf(ds['lon'], ds['lat'], (mpcalc.wind_speed((ds['ugrd10m'][0, t, :, :] *units('m/s')), (ds['vgrd10m'][0, t, :, :] *units('m/s'))) * 2.23694), cmap=cmap, transform=datacrs, levels=speeds, alpha=0.35, extend='max')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=speed_ticks)
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
    
    
            else:
                
                stn.plot_barb((ds['ugrd10m'][t, ::decimate, ::decimate] * 2.23694), (ds['vgrd10m'][t, ::decimate, ::decimate] * 2.23694), color='black', alpha=1, zorder=3, linewidth=0.5)
    
                c = ax.contour(ds['lon'], ds['lat'], (ds['prmslmsl'][t, :, :]/100), levels=mslp_levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                ax.clabel(c, levels=mslp_levels, inline=True, fontsize=8, rightside_up=True)
                
                cs = ax.contourf(ds['lon'], ds['lat'], (mpcalc.wind_speed((ds['ugrd10m'][t, :, :] *units('m/s')), (ds['vgrd10m'][t, :, :] *units('m/s'))) * 2.23694), cmap=cmap, transform=datacrs, levels=speeds, alpha=0.35, extend='max')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=speed_ticks)
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
        print(f"Saved forecast graphics to {path_print}.")

class temperature:

    r'''
    This class hosts the functions showing the temperature forecast.

    '''


    def plot_2m_temperatures(model, region, start_of_warm_season_month=4, end_of_warm_season_month=10, start_of_cool_season_month=11, end_of_cool_season_month=3, temp_scale_warm_start=10, temp_scale_warm_stop=110, temp_scale_cool_start=-20, temp_scale_cool_stop=80, temp_scale_step=1, temperature_contour_value=32, data=False, ds=None, ds_list=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

        r'''
        This function plots the 2-Meter Temperature Forecast. 

        Required Arguments: 
        
        1) model (String) - This is the model the user must select. 
                               
           Here are the choices: 
           1) GFS0p25 - GFS 0.25x0.25 degree
           2) GFS0p50 - GFS 0.5x0.5 degree
           3) GFS1p00 - GFS 1.0x1.0 degree
           4) GEFS0p50 - GEFS 0.5x0.5 degree
           5) CMCENS - Canadian Ensemble
           6) NAM - North American Model
           7) NA NAM - 32km North American Model - Full North America
           8) RAP - Rapid Refresh Model
           9) RAP 32 - 32km Rapid Refresh Model - Full North America
           10) GEFS0p25 ENS MEAN - GEFS 0.25x0.25 degree Ensemble Mean

    2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                         To look at any state use the 2-letter abbreviation for the state in either all capitals
                         or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                         CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                         North America use either: NA, na, North America or north america. If the user wishes to use custom
                         boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                         the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                         'oscc' for South Ops. 

        Optional Arguments: 
        
        1) start_of_warm_season_month (Integer) - Default = 4 (April). The numeric value for the month the warm season begins. 

        2) end_of_warm_season_month (Integer) - Default = 10 (October). The numeric value for the month the warm season ends. 

        3) start_of_cool_season_month (Integer) - Default = 11 (November). The numeric value for the month the cool season begins. 

        4) end_of_cool_season_month (Integer) - Default = 3 (March). The numeric value for the month the cool season ends.

        5) temp_scale_warm_start (Integer) - Default = 10. The bottom bound temperature value in Fahrenheit of the warm season temperature range. 

        6) temp_scale_warm_stop (Integer) - Default = 110. The top bound temperature value in Fahrenheit of the warm season temperature range.

        7) temp_scale_cool_start (Integer) - Default = -20. The bottom bound temperature value in Fahrenheit of the cool season temperature range. 

        8) temp_scale_cool_stop (Integer) - Default = 80. The top bound temperature value in Fahrenheit of the cool season temperature range. 

        9) temp_scale_step (Integer) - Default = 1. The interval at which the temperature scale increases/decreases by in Fahrenheit. 
                                       (Example: temp_scale_step = 5 means the plot will be contoured every 5 degrees Fahrenheit)

        10) temperature_contour_value (Integer) - Default = 32. This draws a contour line seperating two groups of temperature values. 
                                                  Default is the boundary between below and above freezing temperatures.

        11) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                            and passing the data in or if the function needs to download the data. A value of False means the data
                            is downloaded inside of the function while a value of True means the user is downloading the data outside
                            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                            things, it is recommended to set this value to True and download the data outside of the function and pass
                            it in so that the amount of data requests on the host servers can be minimized. 

        12) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                        in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                        outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

        13) ds_list (List) - Default = None. This is the list of datasets the user passes in if the user downloads the data outside of the function
                            and passes in the list of datasets. This is used when the user wishes to plot the 'GEFS0p25 ENS MEAN' since that data
                            needs to be downloaded via HTTPS as it is unavailable on the OpenDAP. If the user wishes to download the data inside of the function, this value is None.

        14) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        15) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        16) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                     

        17) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

        18) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        19) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
                               

        20) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        21) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        22) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        23) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        24) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        25) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        26) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        27) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

        28) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

        29) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

        30) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

        31) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

        32) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

        33) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

        34) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

        35) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        36) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        37) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        38) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        39) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        40) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        41) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'.    

        42) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        43) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        44) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        45) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        46) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        47) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        48) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                          This is a feature of matplotlib, as per their definition, the shrink is:
                                          "Fraction by which to multiply the size of the colorbar." 
                                          This should only be changed if the user wishes to make a custom plot. 
                                          Preset values are called from the settings module for each region. 

        49) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                 Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                 when making a custom plot. 

        50) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

        51) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        52) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

        53) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

        54) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


        Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level


        '''
    
        data=data
        ds=ds
        western_bound=western_bound
        eastern_bound=eastern_bound 
        southern_bound=southern_bound
        northern_bound=northern_bound
        show_rivers=show_rivers
        reference_system=reference_system
        state_border_linewidth=state_border_linewidth
        county_border_linewidth=county_border_linewidth
        gacc_border_linewidth=gacc_border_linewidth
        psa_border_linewidth=psa_border_linewidth 
        cwa_border_linewidth=cwa_border_linewidth
        nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
        nws_public_zones_linewidth=nws_public_zones_linewidth 
        state_border_linestyle=state_border_linestyle
        county_border_linestyle=county_border_linestyle
        gacc_border_linestyle=gacc_border_linestyle
        psa_border_linestyle=psa_border_linestyle 
        cwa_border_linestyle=cwa_border_linestyle
        nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
        nws_public_zones_linestyle=nws_public_zones_linestyle
        x1=x1 
        y1=y1
        x2=x2
        y2=y2 
        x3=x3
        y3=y3 
        shrink=shrink
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        temp_scale_cool_stop_corrected = temp_scale_cool_stop + temp_scale_step
        temp_scale_warm_stop_corrected = temp_scale_warm_stop + temp_scale_step
    
        temp_scale_cool = np.arange(temp_scale_cool_start, temp_scale_cool_stop_corrected, temp_scale_step)
    
        temp_scale_warm = np.arange(temp_scale_warm_start, temp_scale_warm_stop_corrected, temp_scale_step)
    
        ticks_warm = temp_scale_warm[::5]
        ticks_cool = temp_scale_cool[::5]
    
        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            mapcrs = ccrs.LambertConformal()
        else:
            mapcrs = ccrs.PlateCarree()
    
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

        str_level = f"SURFACE"

        path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, '2-Meter Temperature', str_level)
    
        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass

        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
            step = 1
        
        if model == 'CMCENS' or model == 'GEFS0p50':
            step = 1
            
        if model == 'GFS0p25' or model == 'GFS0p25_1h':
            step = 2
            
        if model == 'GFS0p50':
            step = 2
        
        if model == 'GFS1p00':
            step = 2
    
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
            wb=western_bound
            eb=eastern_bound
            sb=southern_bound
            nb=northern_bound
            x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
        else:
            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
            sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)

            if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
                
                if region == 'conus' or region == 'North America' or region == 'north america' or region == 'NA' or region == 'na':
                    decimate = decimate * 2
                else:
                    decimate = decimate + 1
                    
            elif model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
                if region == 'conus' or region == 'North America' or region == 'north america' or region == 'NA' or region == 'na':
                    decimate = decimate * 2
                else:
                    decimate = decimate + 2
            else:
                decimate = decimate
        
        if data == False and model != 'GEFS0p25 ENS MEAN':
            if model == 'RAP' or model == 'RAP 32':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
            else:
                ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)

        if data == False and model == 'GEFS0p25 ENS MEAN':
            ds_list = model_data.get_nomads_model_data_via_https(model, region, 'heightAboveGround', wb, eb, sb, nb, get_u_and_v_wind_components=False, add_wind_gusts=False)
            
        if data == True and model != 'GEFS0p25 ENS MEAN':
            ds = ds

        if data == True and model == 'GEFS0p25 ENS MEAN':
            ds_list = ds_list
    
        cmap = colormaps.temperature_colormap()

        if model != 'GEFS0p25 ENS MEAN':
    
            end1 = (int(round((len(ds['time']) - 1)/6, 0)) - 1)
            end2 = len(ds['time']) - 1
            time = ds['time']
            times = time.to_pandas()
            
            for t in range(0, end1, 1):
            
                fname = f"Image_{t}.png"
            
                fig = plt.figure(figsize=(12, 12))
                fig.set_facecolor('aliceblue')
                
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([wb, eb, sb, nb], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
                ax.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
                ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
                ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
                ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
                else:
                    pass
            
                if show_gacc_borders == True:
                    ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                else:
                    pass
                if show_psa_borders == True:
                    ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                else:
                    pass
                if show_county_borders == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                else:
                    pass
                if show_state_borders == True:
                    ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                else:
                    pass
                if show_cwa_borders == True:
                    ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                else:
                    pass
                if show_nws_firewx_zones == True:
                    ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                else:
                    pass
                if show_nws_public_zones == True:
                    ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                else:
                    pass
        
                model = model.upper()
                plt.title(f"{model} 2-METER TEMPERATURE [°F]", fontsize=9, fontweight='bold', loc='left')
                plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
                ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
                ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
                ax.text(x, y, f"Contour Line: T = {temperature_contour_value}[°F]", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
                
                lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
        
                stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                                 transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
        
                if model == 'CMCENS' or model == 'GEFS0P50':
        
                    temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][0, t, :, :])
        
                    temp = temp[::decimate, ::decimate].to_numpy().flatten()
            
                    stn.plot_parameter('C', temp, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
                       
                    c = ax.contour(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][0, t, :, :]), levels=[temperature_contour_value], colors='purple', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c, levels=[temperature_contour_value], inline=True, fontsize=8, rightside_up=True)
        
                    if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                        cs = ax.contourf(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][0, t, :, :]), cmap=cmap, transform=datacrs, levels=temp_scale_warm, alpha=0.35, extend='both')
                        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_warm)
        
                    if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                        cs = ax.contourf(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][0, t, :, :]), cmap=cmap, transform=datacrs, levels=temp_scale_cool, alpha=0.35, extend='both')
                        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_cool)
        
                    fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                    plt.close(fig)
                    if mapcrs == datacrs:
                        tim.sleep(10)
        
        
                else:
                    
                    temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][t, :, :])
        
                    temp = temp[::decimate, ::decimate].to_numpy().flatten()
            
                    stn.plot_parameter('C', temp, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
                       
                    c = ax.contour(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][t, :, :]), levels=[temperature_contour_value], colors='purple', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c, levels=[temperature_contour_value], inline=True, fontsize=8, rightside_up=True)
        
                    if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                        cs = ax.contourf(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][t, :, :]), cmap=cmap, transform=datacrs, levels=temp_scale_warm, alpha=0.35, extend='both')
                        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_warm)
        
                    if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                        cs = ax.contourf(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][t, :, :]), cmap=cmap, transform=datacrs, levels=temp_scale_cool, alpha=0.35, extend='both')
                        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_cool)
            
                    fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                    plt.close(fig)
                    if mapcrs == datacrs:
                        tim.sleep(10)
        
            for t in range(end1, end2, step):
            
                fname = f"Image_{t}.png"
            
                fig = plt.figure(figsize=(12, 12))
                fig.set_facecolor('aliceblue')
                
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([wb, eb, sb, nb], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
                ax.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
                ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
                ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
                ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
                else:
                    pass
            
                if show_gacc_borders == True:
                    ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                else:
                    pass
                if show_psa_borders == True:
                    ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                else:
                    pass
                if show_county_borders == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                else:
                    pass
                if show_state_borders == True:
                    ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                else:
                    pass
                if show_cwa_borders == True:
                    ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                else:
                    pass
                if show_nws_firewx_zones == True:
                    ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                else:
                    pass
                if show_nws_public_zones == True:
                    ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                else:
                    pass
        
                model = model.upper()
                plt.title(f"{model} 2-METER TEMPERATURE [°F]", fontsize=9, fontweight='bold', loc='left')
                plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
                ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
                ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
                ax.text(x, y, f"Contour Line: T = {temperature_contour_value}[°F]", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
                
                lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
        
                stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                                 transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
        
                if model == 'CMCENS' or model == 'GEFS0P50':
        
                    temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][0, t, :, :])
        
                    temp = temp[::decimate, ::decimate].to_numpy().flatten()
            
                    stn.plot_parameter('C', temp, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
                       
                    c = ax.contour(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][0, t, :, :]), levels=[temperature_contour_value], colors='purple', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c, levels=[temperature_contour_value], inline=True, fontsize=8, rightside_up=True)
        
                    if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                        cs = ax.contourf(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][0, t, :, :]), cmap=cmap, transform=datacrs, levels=temp_scale_warm, alpha=0.35, extend='both')
                        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_warm)
        
                    if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                        cs = ax.contourf(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][0, t, :, :]), cmap=cmap, transform=datacrs, levels=temp_scale_cool, alpha=0.35, extend='both')
                        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_cool)
        
                    fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                    plt.close(fig)
                    if mapcrs == datacrs:
                        tim.sleep(10)
        
        
                else:
                    
                    temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][t, :, :])
        
                    temp = temp[::decimate, ::decimate].to_numpy().flatten()
            
                    stn.plot_parameter('C', temp, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
                       
                    c = ax.contour(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][t, :, :]), levels=[temperature_contour_value], colors='purple', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c, levels=[temperature_contour_value], inline=True, fontsize=8, rightside_up=True)
        
                    if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                        cs = ax.contourf(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][t, :, :]), cmap=cmap, transform=datacrs, levels=temp_scale_warm, alpha=0.35, extend='both')
                        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_warm)
        
                    if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                        cs = ax.contourf(ds['lon'], ds['lat'], unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'][t, :, :]), cmap=cmap, transform=datacrs, levels=temp_scale_cool, alpha=0.35, extend='both')
                        cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_cool)
            
                    fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                    plt.close(fig)
                    if mapcrs == datacrs:
                        tim.sleep(10)
            print(f"Saved forecast graphics to {path_print}.")

        if model == 'GEFS0p25 ENS MEAN':
    
            for i in range(0, (len(ds_list) - 1)):

                time = ds_list[i]['valid_time']
                init = ds_list[0]['time']
                times = time.to_pandas()
                times = pd.to_datetime(times)
                inits = init.to_pandas()
                inits = pd.to_datetime(inits)
                
                tempK = ds_list[i]['t2m']
                temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(tempK)
                c_temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(tempK)

                fname = f"Image_{i}.png"
            
                fig = plt.figure(figsize=(12, 12))
                fig.set_facecolor('aliceblue')
                
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([wb, eb, sb, nb], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
                ax.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
                ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
                ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
                ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
                else:
                    pass
            
                if show_gacc_borders == True:
                    ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                else:
                    pass
                if show_psa_borders == True:
                    ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                else:
                    pass
                if show_county_borders == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                else:
                    pass
                if show_state_borders == True:
                    ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                else:
                    pass
                if show_cwa_borders == True:
                    ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                else:
                    pass
                if show_nws_firewx_zones == True:
                    ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                else:
                    pass
                if show_nws_public_zones == True:
                    ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                else:
                    pass
        
                model = model.upper()
                
                plt.title(f"{model} 2-METER TEMPERATURE [°F]", fontsize=9, fontweight='bold', loc='left')
                plt.title("Forecast Valid: " +times.strftime('%a %d/%H UTC')+"\nInitialization: "+inits.strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
                ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
                ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
                ax.text(x, y, f"Contour Line: T = {temperature_contour_value}[°F]", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
            
                lon_2d, lat_2d = np.meshgrid(ds_list[i]['longitude'], ds_list[i]['latitude'])
    
                numbers = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                                 transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
                
    
                temp = temp[::decimate, ::decimate].to_numpy().flatten()
        
                numbers.plot_parameter('C', temp, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

                c = ax.contour(ds_list[i]['longitude'], ds_list[i]['latitude'], c_temp[: , :], levels=[temperature_contour_value], colors='purple', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                ax.clabel(c, levels=[temperature_contour_value], inline=True, fontsize=8, rightside_up=True)

    
                if utc_time.month >= start_of_warm_season_month and utc_time.month <= end_of_warm_season_month:
                    cs = ax.contourf(ds_list[i]['longitude'], ds_list[i]['latitude'], c_temp[: , :], cmap=cmap, transform=datacrs, levels=temp_scale_warm, alpha=0.35, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_warm)
    
                if utc_time.month >= start_of_cool_season_month or utc_time.month <= end_of_cool_season_month:
                    cs = ax.contourf(ds_list[i]['longitude'], ds_list[i]['latitude'], c_temp[: , :], cmap=cmap, transform=datacrs, levels=temp_scale_cool, alpha=0.35, extend='both')
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks_cool)
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
            print(f"Saved forecast graphics to {path_print}.")


    def plot_freezing_level(model, region, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

        r'''
        This function plots the Freezing Level Forecast. 

        Required Arguments: 
        
        1) model (String) - This is the model the user must select. 
                               
           Here are the choices: 
           1) GFS0p25 - GFS 0.25x0.25 degree
           2) GFS0p50 - GFS 0.5x0.5 degree
           3) GFS1p00 - GFS 1.0x1.0 degree
           4) GEFS0p50 - GEFS 0.5x0.5 degree
           5) CMCENS - Canadian Ensemble
           6) NAM - North American Model
           7) NA NAM - 32km North American Model - Full North America
           8) RAP - Rapid Refresh Model
           9) RAP 32 - 32km Rapid Refresh Model - Full North America
    
        2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                             To look at any state use the 2-letter abbreviation for the state in either all capitals
                             or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                             CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                             North America use either: NA, na, North America or north america. If the user wishes to use custom
                             boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                             the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                             'oscc' for South Ops. 

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

        3) ds_list (List) - Default = None. This is the list of datasets the user passes in if the user downloads the data outside of the function
                            and passes in the list of datasets. This is used when the user wishes to plot the 'GEFS0p25 ENS MEAN' since that data
                            needs to be downloaded via HTTPS as it is unavailable on the OpenDAP. If the user wishes to download the data inside of the function, this value is None.

        4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                     

        7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

        8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        9) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
                               

        10) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        11) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        12) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        13) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        14) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        15) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        16) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

        18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

        19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

        20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

        21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

        22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

        23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

        24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

        25) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        26) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        27) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        28) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        29) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        30) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        31) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'.    

        32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                          This is a feature of matplotlib, as per their definition, the shrink is:
                                          "Fraction by which to multiply the size of the colorbar." 
                                          This should only be changed if the user wishes to make a custom plot. 
                                          Preset values are called from the settings module for each region. 

        39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                 Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                 when making a custom plot. 

        40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

        41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

        43) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

        44) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


        Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/FREEZING LEVEL


        '''
    
        data=data
        ds=ds
        western_bound=western_bound
        eastern_bound=eastern_bound 
        southern_bound=southern_bound
        northern_bound=northern_bound
        show_rivers=show_rivers
        reference_system=reference_system
        state_border_linewidth=state_border_linewidth
        county_border_linewidth=county_border_linewidth
        gacc_border_linewidth=gacc_border_linewidth
        psa_border_linewidth=psa_border_linewidth 
        cwa_border_linewidth=cwa_border_linewidth
        nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
        nws_public_zones_linewidth=nws_public_zones_linewidth 
        state_border_linestyle=state_border_linestyle
        county_border_linestyle=county_border_linestyle
        gacc_border_linestyle=gacc_border_linestyle
        psa_border_linestyle=psa_border_linestyle 
        cwa_border_linestyle=cwa_border_linestyle
        nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
        nws_public_zones_linestyle=nws_public_zones_linestyle
        x1=x1 
        y1=y1
        x2=x2
        y2=y2 
        x3=x3
        y3=y3 
        shrink=shrink
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        levels = np.arange(3000, 10500, 500)
        ticks = levels[::2]
    
        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            mapcrs = ccrs.LambertConformal()
        else:
            mapcrs = ccrs.PlateCarree()
    
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

        str_level = f"FREEZING LEVEL"

        path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, 'Freezing Level', str_level)
    
        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass

        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
            step = 1
        
        if model == 'GEFS0p50':
            step = 1
            
        if model == 'GFS0p25' or model == 'GFS0p25_1h':
            step = 2
            
        if model == 'GFS0p50':
            step = 2
        
        if model == 'GFS1p00':
            step = 2
    
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
            wb=western_bound
            eb=eastern_bound
            sb=southern_bound
            nb=northern_bound
            x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
        else:
            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
            sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)

            if model == 'GFS0p25' or model == 'NAM' or model == 'NAM 1hr' or model == 'GFS0p25_1hr':
                decimate = decimate * 2
            else:
                decimate = decimate
        
        if data == False:
            if model == 'RAP' or model == 'RAP 32':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
            else:
                ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
            
        if data == True:
            ds = ds
    
        cmap = colormaps.gph_colormap()
    
        end1 = (int(round((len(ds['time']) - 1)/6, 0)) - 1)
        end2 = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()
        
        for t in range(0, end1, 1):
        
            fname = f"Image_{t}.png"
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
            ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            model = model.upper()
            plt.title(f"{model} FREEZING LEVEL [FT]", fontsize=9, fontweight='bold', loc='left')
            plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
            
            lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
    
            stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                             transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
    
            if model == 'GEFS0P50':
    
                hgt = ds['hgttop0c'][0, t, :, :] * 3.28084
    
                hgt = hgt[::decimate, ::decimate].to_numpy().flatten()
        
                stn.plot_parameter('C', hgt, color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

                cs = ax.contourf(ds['lon'], ds['lat'], (ds['hgttop0c'][0, t, :, :] * 3.28084), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
    
    
            else:
                
                hgt = ds['hgttop0c'][t, :, :] * 3.28084
    
                hgt = hgt[::decimate, ::decimate].to_numpy().flatten()
        
                stn.plot_parameter('C', hgt, color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

                cs = ax.contourf(ds['lon'], ds['lat'], (ds['hgttop0c'][t, :, :] * 3.28084), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
    
        for t in range(end1, end2, step):
        
            fname = f"Image_{t}.png"
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            model = model.upper()
            plt.title(f"{model} FREEZING LEVEL [FT]", fontsize=9, fontweight='bold', loc='left')
            plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
            
            lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
    
            stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                             transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
    
            if model == 'GEFS0P50':
    
                hgt = ds['hgttop0c'][0, t, :, :] * 3.28084
    
                hgt = hgt[::decimate, ::decimate].to_numpy().flatten()
        
                stn.plot_parameter('C', hgt, color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

                cs = ax.contourf(ds['lon'], ds['lat'], (ds['hgttop0c'][0, t, :, :] * 3.28084), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
    
    
            else:
                
                hgt = ds['hgttop0c'][t, :, :] * 3.28084
    
                hgt = hgt[::decimate, ::decimate].to_numpy().flatten()
        
                stn.plot_parameter('C', hgt, color='white', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

                cs = ax.contourf(ds['lon'], ds['lat'], (ds['hgttop0c'][t, :, :] * 3.28084), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
        print(f"Saved forecast graphics to {path_print}.")


    def plot_heights_temperature_wind(model, region, level=850, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8):

        r'''
        This function plots the Geopotential Height/Temperature/Wind Forecast for a specific level. 

        Required Arguments: 
        
        1) model (String) - This is the model the user must select. 
                               
           Here are the choices: 
           1) GFS0p25 - GFS 0.25x0.25 degree
           2) GFS0p50 - GFS 0.5x0.5 degree
           3) GFS1p00 - GFS 1.0x1.0 degree
           4) GEFS0p50 - GEFS 0.5x0.5 degree
           5) CMCENS - Canadian Ensemble
           6) NAM - North American Model
           7) NA NAM - 32km North American Model - Full North America
           8) RAP - Rapid Refresh Model
           9) RAP 32 - 32km Rapid Refresh Model - Full North America

        2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                             To look at any state use the 2-letter abbreviation for the state in either all capitals
                             or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                             CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                             North America use either: NA, na, North America or north america. If the user wishes to use custom
                             boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                             the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                             'oscc' for South Ops. 

        Optional Arguments: 
        
        1) level (Integer) - Default = 850. This is the level in millibars or hectopascals at which the user wishes to examine. 
                             850 means 850mb or 850hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

        2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                            and passing the data in or if the function needs to download the data. A value of False means the data
                            is downloaded inside of the function while a value of True means the user is downloading the data outside
                            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                            things, it is recommended to set this value to True and download the data outside of the function and pass
                            it in so that the amount of data requests on the host servers can be minimized. 

        3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                        in the dataset. If the user wishes to download the data inside of the function, this value is None. 

        4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                     

        7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

        8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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
                               

        10) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        11) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        12) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        13) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        14) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        15) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        16) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

        18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

        19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

        20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

        21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

        22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

        23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

        24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

        25) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        26) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        27) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        28) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        29) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        30) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        31) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'.    

        32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                          This is a feature of matplotlib, as per their definition, the shrink is:
                                          "Fraction by which to multiply the size of the colorbar." 
                                          This should only be changed if the user wishes to make a custom plot. 
                                          Preset values are called from the settings module for each region. 

        39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                 Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                 when making a custom plot. 

        40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

        41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.


        Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

        '''
    
        data=data
        level=level
        ds=ds
        western_bound=western_bound
        eastern_bound=eastern_bound 
        southern_bound=southern_bound
        northern_bound=northern_bound
        show_rivers=show_rivers
        reference_system=reference_system
        state_border_linewidth=state_border_linewidth
        county_border_linewidth=county_border_linewidth
        gacc_border_linewidth=gacc_border_linewidth
        psa_border_linewidth=psa_border_linewidth 
        cwa_border_linewidth=cwa_border_linewidth
        nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
        nws_public_zones_linewidth=nws_public_zones_linewidth 
        state_border_linestyle=state_border_linestyle
        county_border_linestyle=county_border_linestyle
        gacc_border_linestyle=gacc_border_linestyle
        psa_border_linestyle=psa_border_linestyle 
        cwa_border_linestyle=cwa_border_linestyle
        nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
        nws_public_zones_linestyle=nws_public_zones_linestyle
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            mapcrs = ccrs.LambertConformal()
        else:
            mapcrs = ccrs.PlateCarree()
    
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
    
        str_level = f"{level} MB"
    
        if level == 850:
            hgt_levels = np.arange(96, 180, 4)
            temp_levels = np.arange(-40, 31, 1)
        if level == 700:
            hgt_levels = np.arange(240, 340, 4)
            temp_levels = np.arange(-50, 21, 1)
        if level == 500:
            temp_levels = np.arange(-60, 11, 1)
        if level == 300:
            hgt_levels = np.arange(840, 1020, 10)
            temp_levels = np.arange(-60, -19, 1)
        if level == 250:
            hgt_levels = np.arange(900, 1140, 10)
            temp_levels = np.arange(-70, -29, 1)
        if level == 200:
            hgt_levels = np.arange(1000, 1280, 10)
            temp_levels = np.arange(-70, -29, 1)

        ticks = temp_levels[::5]        

        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america' or region == 'conus' or region == 'CONUS' or region == 'CONUS & South Canada & North Mexico':

            temp_low_levels = np.arange(-60, 0, 10)
            temp_high_levels = np.arange(10, 50, 10)
            
        else:

            temp_low_levels = np.arange(-60, 0, 5)
            temp_high_levels = np.arange(5, 55, 10)            
    
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
            decimate = 20
            step = 1
            
            if level == 850:
                level_idx = 6
            if level == 700:
                level_idx = 12
            if level == 500:
                level_idx = 20
            if level == 300:
                level_idx = 28
            if level == 250:
                level_idx = 30
            if level == 200:
                level_idx = 32
        
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 10
            step = 1
    
            if level == 850:
                level_idx = 2
            if level == 700:
                level_idx = 3
            if level == 500:
                level_idx = 4
            if level == 300:
                level_idx = 6
            if level == 250:
                level_idx = 7
            if level == 200:
                level_idx = 8
            
        if model == 'GFS0p25' or model == 'GFS0p25_1h':
            decimate = 10
            step = 2
            
            if level == 850:
                level_idx = 5
            if level == 700:
                level_idx = 8
            if level == 500:
                level_idx = 12
            if level == 300:
                level_idx = 16
            if level == 250:
                level_idx = 17
            if level == 200:
                level_idx = 18
            
        if model == 'GFS0p50':
            decimate = 10
            step = 2
            
            if level == 850:
                level_idx = 6
            if level == 700:
                level_idx = 12
            if level == 500:
                level_idx = 20
            if level == 300:
                level_idx = 28
            if level == 250:
                level_idx = 30
            if level == 200:
                level_idx = 32
        
        if model == 'GFS1p00':
            decimate = 10
            step = 2
    
            if level == 850:
                level_idx = 5
            if level == 700:
                level_idx = 8
            if level == 500:
                level_idx = 12
            if level == 300:
                level_idx = 16
            if level == 250:
                level_idx = 17
            if level == 200:
                level_idx = 18
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
            wb=western_bound
            eb=eastern_bound
            sb=southern_bound
            nb=northern_bound
            x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
        else:
            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
            sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)
        
        if data == False:
            if model == 'RAP' or model == 'RAP 32':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
            else:
                ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
            
        if data == True:
            ds = ds
    
    
        cmap = colormaps.temperature_colormap_alt()
    
        end = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()
    
    
        path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, 'Height Temperature Wind', str_level)
    
        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass

        for t in range(0, end, step):
        
            fname = f"Image_{t}.png"
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            model = model.upper()
            plt.title(f"{model} {str_level} GPH [DM]/TEMPERATURE [°C]/WIND [KTS]", fontsize=9, fontweight='bold', loc='left')
            plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
            
            lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
            
            stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                             transform=ccrs.PlateCarree(), zorder=3, fontsize=5, clip_on=True)
    
    
            if model == 'CMCENS' or model == 'GEFS0P50':
    
                stn.plot_barb((ds['ugrdprs'][0, t, level_idx, ::decimate, ::decimate] * 1.94384), (ds['vgrdprs'][0, t, level_idx, ::decimate, ::decimate] * 1.94384), color='black', alpha=1, zorder=3, linewidth=0.25)
    
                if level == 500:
                    c_neg = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=np.arange(440, 540, 4), colors='black', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                    c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=[540], colors='black', zorder=2, transform=datacrs, linewidths=1)
                    c_pos = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=np.arange(544, 624, 4), colors='black', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                    ax.clabel(c_neg, levels=np.arange(440, 540, 4), inline=True, fontsize=8, rightside_up=True)
                    ax.clabel(c, levels=[540], inline=True, fontsize=8, rightside_up=True)
                    ax.clabel(c_pos, levels=np.arange(544, 624, 4), inline=True, fontsize=8, rightside_up=True)
    
                else:                
                    c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=hgt_levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                    ax.clabel(c, levels=hgt_levels, inline=True, fontsize=8, rightside_up=True)

                c_temp_below = ax.contour(ds['lon'], ds['lat'], (ds['tmpprs'][0, t, level_idx, :, :] - 273.15), colors='purple', transform=datacrs, levels=temp_low_levels, linewidths=0.5, linestyles='--')
                ax.clabel(c_temp_below, levels=temp_low_levels, inline=True, fontsize=8, rightside_up=True)

                c_temp_0 = ax.contour(ds['lon'], ds['lat'], (ds['tmpprs'][0, t, level_idx, :, :] - 273.15), colors='dimgrey', transform=datacrs, levels=[0], linewidths=0.5, linestyles='--')
                ax.clabel(c_temp_0, levels=[0], inline=True, fontsize=8, rightside_up=True)

                c_temp_above = ax.contour(ds['lon'], ds['lat'], (ds['tmpprs'][0, t, level_idx, :, :] - 273.15), colors='darkorange', transform=datacrs, levels=temp_high_levels, linewidths=0.5, linestyles='--')
                ax.clabel(c_temp_above, levels=temp_high_levels, inline=True, fontsize=8, rightside_up=True)
                    
                cs = ax.contourf(ds['lon'], ds['lat'], (ds['tmpprs'][0, t, level_idx, :, :] - 273.15), cmap=cmap, transform=datacrs, levels=temp_levels, alpha=0.35, extend='both')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
    
    
            else:
                
                stn.plot_barb((ds['ugrdprs'][t, level_idx, ::decimate, ::decimate] * 1.94384), (ds['vgrdprs'][t, level_idx, ::decimate, ::decimate] * 1.94384), color='black', alpha=1, zorder=3, linewidth=0.25)
    
                if level == 500:
                    c_neg = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=np.arange(440, 540, 4), colors='black', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                    c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=[540], colors='black', zorder=2, transform=datacrs, linewidths=1)
                    c_pos = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=np.arange(544, 624, 4), colors='black', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                    ax.clabel(c_neg, levels=np.arange(440, 540, 4), inline=True, fontsize=8, rightside_up=True)
                    ax.clabel(c, levels=[540], inline=True, fontsize=8, rightside_up=True)
                    ax.clabel(c_pos, levels=np.arange(544, 624, 4), inline=True, fontsize=8, rightside_up=True)
    
                else:
                    c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=hgt_levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                    ax.clabel(c, levels=hgt_levels, inline=True, fontsize=8, rightside_up=True)

                c_temp_below = ax.contour(ds['lon'], ds['lat'], (ds['tmpprs'][t, level_idx, :, :] - 273.15), colors='purple', transform=datacrs, levels=temp_low_levels, linewidths=0.5, linestyles='--')
                ax.clabel(c_temp_below, levels=temp_low_levels, inline=True, fontsize=8, rightside_up=True)

                c_temp_0 = ax.contour(ds['lon'], ds['lat'], (ds['tmpprs'][t, level_idx, :, :] - 273.15), colors='dimgrey', transform=datacrs, levels=[0], linewidths=0.5, linestyles='--')
                ax.clabel(c_temp_0, levels=[0], inline=True, fontsize=8, rightside_up=True)

                c_temp_above = ax.contour(ds['lon'], ds['lat'], (ds['tmpprs'][t, level_idx, :, :] - 273.15), colors='darkorange', transform=datacrs, levels=temp_high_levels, linewidths=0.5, linestyles='--')
                ax.clabel(c_temp_above, levels=temp_high_levels, inline=True, fontsize=8, rightside_up=True)
                
                cs = ax.contourf(ds['lon'], ds['lat'], (ds['tmpprs'][t, level_idx, :, :] - 273.15), cmap=cmap, transform=datacrs, levels=temp_levels, alpha=0.35, extend='both')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
        print(f"Saved forecast graphics to {path_print}.")


class relative_humidity:

    r'''
    This class hosts the functions that plot the relative humidity forecast graphics. 

    '''

    def plot_2m_relative_humidity(model, region, low_rh_threshold=15, data=False, ds=None, ds_list=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

        r'''
        This function plots the 2-Meter Relative Humidity Forecast. 

        Required Arguments: 
        
        1) model (String) - This is the model the user must select. 
                               
           Here are the choices: 
           1) GFS0p25 - GFS 0.25x0.25 degree
           2) GFS0p50 - GFS 0.5x0.5 degree
           3) GFS1p00 - GFS 1.0x1.0 degree
           4) GEFS0p50 - GEFS 0.5x0.5 degree
           5) CMCENS - Canadian Ensemble
           6) NAM - North American Model
           7) NA NAM - 32km North American Model - Full North America
           8) RAP - Rapid Refresh Model
           9) RAP 32 - 32km Rapid Refresh Model - Full North America
           10) GEFS0p25 ENS MEAN - GEFS 0.25x0.25 degree Ensemble Mean

        2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                             To look at any state use the 2-letter abbreviation for the state in either all capitals
                             or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                             CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                             North America use either: NA, na, North America or north america. If the user wishes to use custom
                             boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                             the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                             'oscc' for South Ops. 

        Optional Arguments: 
        
        1) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                            and passing the data in or if the function needs to download the data. A value of False means the data
                            is downloaded inside of the function while a value of True means the user is downloading the data outside
                            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                            things, it is recommended to set this value to True and download the data outside of the function and pass
                            it in so that the amount of data requests on the host servers can be minimized. 

        2) low_rh_threshold (Integer) - Default = 15. The threshold for the contour line that defines what extremely low relative humidity is. 

        3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                        in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                        outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

        4) ds_list (List) - Default = None. This is the list of datasets the user passes in if the user downloads the data outside of the function
                            and passes in the list of datasets. This is used when the user wishes to plot the 'GEFS0p25 ENS MEAN' since that data
                            needs to be downloaded via HTTPS as it is unavailable on the OpenDAP. If the user wishes to download the data inside of the function, this value is None.

        5) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        6) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        7) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                     

        8) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

        9) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        10) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
                               

        11) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        12) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        13) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        14) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        15) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        16) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        17) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        18) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

        19) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

        20) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

        21) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

        22) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

        23) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

        24) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

        25) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

        26) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        27) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        28) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        29) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        30) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        31) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        32) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'.    

        33) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        34) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        35) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        36) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        37) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        38) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        39) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                          This is a feature of matplotlib, as per their definition, the shrink is:
                                          "Fraction by which to multiply the size of the colorbar." 
                                          This should only be changed if the user wishes to make a custom plot. 
                                          Preset values are called from the settings module for each region. 

        40) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                 Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                 when making a custom plot. 

        41) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

        42) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        43) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

        44) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

        45) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


        Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level


        '''
    
        data=data
        ds=ds
        western_bound=western_bound
        eastern_bound=eastern_bound 
        southern_bound=southern_bound
        northern_bound=northern_bound
        show_rivers=show_rivers
        reference_system=reference_system
        state_border_linewidth=state_border_linewidth
        county_border_linewidth=county_border_linewidth
        gacc_border_linewidth=gacc_border_linewidth
        psa_border_linewidth=psa_border_linewidth 
        cwa_border_linewidth=cwa_border_linewidth
        nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
        nws_public_zones_linewidth=nws_public_zones_linewidth 
        state_border_linestyle=state_border_linestyle
        county_border_linestyle=county_border_linestyle
        gacc_border_linestyle=gacc_border_linestyle
        psa_border_linestyle=psa_border_linestyle 
        cwa_border_linestyle=cwa_border_linestyle
        nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
        nws_public_zones_linestyle=nws_public_zones_linestyle
        x1=x1 
        y1=y1
        x2=x2
        y2=y2 
        x3=x3
        y3=y3 
        shrink=shrink
        sample_point_fontsize=sample_point_fontsize
        x=x 
        y=y
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        levels = np.arange(0, 101, 1)
        ticks = levels[::5]
    
        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            mapcrs = ccrs.LambertConformal()
        else:
            mapcrs = ccrs.PlateCarree()
    
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
    
        str_level = f"SURFACE"
    
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
            step = 1
        
        if model == 'CMCENS' or model == 'GEFS0p50':
            step = 1
            
        if model == 'GFS0p25' or model == 'GFS0p25_1h':
            step = 2
            
        if model == 'GFS0p50':
            step = 2
        
        if model == 'GFS1p00':
            step = 2
    
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
            wb=western_bound
            eb=eastern_bound
            sb=southern_bound
            nb=northern_bound
            x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
        else:
            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
            sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)

            if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
                
                if region == 'conus' or region == 'North America' or region == 'north america' or region == 'NA' or region == 'na':
                    decimate = decimate * 2
                else:
                    decimate = decimate + 1
                    
            elif model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
                if region == 'conus' or region == 'North America' or region == 'north america' or region == 'NA' or region == 'na':
                    decimate = decimate * 2
                else:
                    decimate = decimate + 2
            else:
                decimate = decimate

        path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, '2-Meter Relative Humidity', str_level)
    
        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass

        if data == False and model != 'GEFS0p25 ENS MEAN':
            if model == 'RAP' or model == 'RAP 32':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
            else:
                ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)

        if data == False and model == 'GEFS0p25 ENS MEAN':
            ds_list = model_data.get_nomads_model_data_via_https(model, region, 'heightAboveGround', wb, eb, sb, nb, get_u_and_v_wind_components=False, add_wind_gusts=False)
            
        if data == True and model != 'GEFS0p25 ENS MEAN':
            ds = ds

        if data == True and model == 'GEFS0p25 ENS MEAN':
            ds_list = ds_list
    
        cmap = colormaps.relative_humidity_colormap()

        if model != 'GEFS0p25 ENS MEAN':
    
            end1 = (int(round((len(ds['time']) - 1)/6, 0)) - 1)
            end2 = len(ds['time']) - 1
            time = ds['time']
            times = time.to_pandas()
            
            for t in range(0, end1, 1):
            
                fname = f"Image_{t}.png"
            
                fig = plt.figure(figsize=(12, 12))
                fig.set_facecolor('aliceblue')
                
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([wb, eb, sb, nb], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
                ax.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
                ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
                ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
                ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
                else:
                    pass
            
                if show_gacc_borders == True:
                    ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                else:
                    pass
                if show_psa_borders == True:
                    ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                else:
                    pass
                if show_county_borders == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                else:
                    pass
                if show_state_borders == True:
                    ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                else:
                    pass
                if show_cwa_borders == True:
                    ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                else:
                    pass
                if show_nws_firewx_zones == True:
                    ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                else:
                    pass
                if show_nws_public_zones == True:
                    ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                else:
                    pass
        
                model = model.upper()
                plt.title(f"{model} 2-METER RELATIVE HUMIDITY [%]", fontsize=9, fontweight='bold', loc='left')
                plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
                ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
                ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
                ax.text(x, y, f"Contour Line: RH = {low_rh_threshold}%", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
                
                lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
        
                stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                                 transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
        
                if model == 'CMCENS' or model == 'GEFS0P50':
        
                    rh = ds['rh2m'][0, t, :, :]
        
                    rh = rh[::decimate, ::decimate].to_numpy().flatten()
            
                    stn.plot_parameter('C', rh, color='pink', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
                       
                    c = ax.contour(ds['lon'], ds['lat'], ds['rh2m'][0, t, :, :], levels=[low_rh_threshold], colors='brown', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c, levels=[low_rh_threshold], inline=True, fontsize=8, rightside_up=True)
        
                    cs = ax.contourf(ds['lon'], ds['lat'], ds['rh2m'][0, t, :, :], cmap=cmap, transform=datacrs, levels=levels, alpha=0.35)
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
        
                    fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                    plt.close(fig)
                    if mapcrs == datacrs:
                        tim.sleep(10)
        
        
                else:
                    
                    rh = ds['rh2m'][t, :, :]
        
                    rh = rh[::decimate, ::decimate].to_numpy().flatten()
            
                    stn.plot_parameter('C', rh, color='pink', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
                       
                    c = ax.contour(ds['lon'], ds['lat'], ds['rh2m'][t, :, :], levels=[low_rh_threshold], colors='brown', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c, levels=[low_rh_threshold], inline=True, fontsize=8, rightside_up=True)
        
                    cs = ax.contourf(ds['lon'], ds['lat'], ds['rh2m'][t, :, :], cmap=cmap, transform=datacrs, levels=levels, alpha=0.35)
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
            
                    fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                    plt.close(fig)
                    if mapcrs == datacrs:
                        tim.sleep(10)
        
            for t in range(end1, end2, step):
            
                fname = f"Image_{t}.png"
            
                fig = plt.figure(figsize=(12, 12))
                fig.set_facecolor('aliceblue')
                
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([wb, eb, sb, nb], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
                ax.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
                ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
                ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
                ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
                else:
                    pass
            
                if show_gacc_borders == True:
                    ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                else:
                    pass
                if show_psa_borders == True:
                    ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                else:
                    pass
                if show_county_borders == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                else:
                    pass
                if show_state_borders == True:
                    ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                else:
                    pass
                if show_cwa_borders == True:
                    ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                else:
                    pass
                if show_nws_firewx_zones == True:
                    ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                else:
                    pass
                if show_nws_public_zones == True:
                    ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                else:
                    pass
        
                model = model.upper()
                plt.title(f"{model} 2-METER RELATIVE HUMIDITY [%]", fontsize=9, fontweight='bold', loc='left')
                plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
                ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
                ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
                ax.text(x, y, f"Contour Line: RH = {low_rh_threshold}%", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
                
                lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
        
                stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                                 transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
        
                if model == 'CMCENS' or model == 'GEFS0P50':
        
                    rh = ds['rh2m'][0, t, :, :]
        
                    rh = rh[::decimate, ::decimate].to_numpy().flatten()
            
                    stn.plot_parameter('C', rh, color='pink', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
                       
                    c = ax.contour(ds['lon'], ds['lat'], ds['rh2m'][0, t, :, :], levels=[low_rh_threshold], colors='brown', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c, levels=[low_rh_threshold], inline=True, fontsize=8, rightside_up=True)
        
                    cs = ax.contourf(ds['lon'], ds['lat'], ds['rh2m'][0, t, :, :], cmap=cmap, transform=datacrs, levels=levels, alpha=0.35)
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
        
                    fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                    plt.close(fig)
                    if mapcrs == datacrs:
                        tim.sleep(10)
        
        
                else:
                    
                    rh = ds['rh2m'][t, :, :]
        
                    rh = rh[::decimate, ::decimate].to_numpy().flatten()
            
                    stn.plot_parameter('C', rh, color='pink', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
                       
                    c = ax.contour(ds['lon'], ds['lat'], ds['rh2m'][t, :, :], levels=[low_rh_threshold], colors='brown', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                    ax.clabel(c, levels=[low_rh_threshold], inline=True, fontsize=8, rightside_up=True)
        
                    cs = ax.contourf(ds['lon'], ds['lat'], ds['rh2m'][t, :, :], cmap=cmap, transform=datacrs, levels=levels, alpha=0.35)
                    cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
            
                    fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                    plt.close(fig)
                    if mapcrs == datacrs:
                        tim.sleep(10)

        if model == 'GEFS0p25 ENS MEAN':
    
            for i in range(0, (len(ds_list) - 1)):

                time = ds_list[i]['valid_time']
                init = ds_list[0]['time']
                times = time.to_pandas()
                times = pd.to_datetime(times)
                inits = init.to_pandas()
                inits = pd.to_datetime(inits)
                
                rh = ds_list[i]['r2']

                fname = f"Image_{i}.png"
            
                fig = plt.figure(figsize=(12, 12))
                fig.set_facecolor('aliceblue')
                
                ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                ax.set_extent([wb, eb, sb, nb], datacrs)
                ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
                ax.add_feature(cfeature.LAND, color='beige', zorder=1)
                ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
                ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
                ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
                ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
                if show_rivers == True:
                    ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
                else:
                    pass
            
                if show_gacc_borders == True:
                    ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                else:
                    pass
                if show_psa_borders == True:
                    ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                else:
                    pass
                if show_county_borders == True:
                    ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                else:
                    pass
                if show_state_borders == True:
                    ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                else:
                    pass
                if show_cwa_borders == True:
                    ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                else:
                    pass
                if show_nws_firewx_zones == True:
                    ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                else:
                    pass
                if show_nws_public_zones == True:
                    ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                else:
                    pass
        
                model = model.upper()
                
                plt.title(f"{model} 2-METER RELATIVE HUMIDITY [%]", fontsize=9, fontweight='bold', loc='left')
                plt.title("Forecast Valid: " +times.strftime('%a %d/%H UTC')+"\nInitialization: "+inits.strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
                ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
                ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
                ax.text(x, y, f"Contour Line: RH = {low_rh_threshold}%", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
             
                lon_2d, lat_2d = np.meshgrid(ds_list[i]['longitude'], ds_list[i]['latitude'])
    
                numbers = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                                 transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
                
    
                rh = rh[::decimate, ::decimate].to_numpy().flatten()
        
                numbers.plot_parameter('C', rh, color='pink', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)

    
                cs = ax.contourf(ds_list[i]['longitude'], ds_list[i]['latitude'], ds_list[i]['r2'][:, :], cmap=cmap, transform=datacrs, levels=levels, alpha=0.35)
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)

                c = ax.contour(ds_list[i]['longitude'], ds_list[i]['latitude'], ds_list[i]['r2'][:, :], levels=[low_rh_threshold], colors='brown', zorder=2, transform=datacrs, linewidths=1, linestyles='--')
                ax.clabel(c, levels=[low_rh_threshold], inline=True, fontsize=8, rightside_up=True)
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
        print(f"Saved forecast graphics to {path_print}.")

    def plot_heights_relative_humidity_wind(model, region, level=700, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8):

        r'''
        This function plots the Geopotential Height/Relative Humidity/Wind Forecast for a specific level. 

        Required Arguments: 
        
        1) model (String) - This is the model the user must select. 
                               
           Here are the choices: 
           1) GFS0p25 - GFS 0.25x0.25 degree
           2) GFS0p50 - GFS 0.5x0.5 degree
           3) GFS1p00 - GFS 1.0x1.0 degree
           4) GEFS0p50 - GEFS 0.5x0.5 degree
           5) CMCENS - Canadian Ensemble
           6) NAM - North American Model
           7) NA NAM - 32km North American Model - Full North America
           8) RAP - Rapid Refresh Model
           9) RAP 32 - 32km Rapid Refresh Model - Full North America

        2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                             To look at any state use the 2-letter abbreviation for the state in either all capitals
                             or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                             CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                             North America use either: NA, na, North America or north america. If the user wishes to use custom
                             boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                             the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                             'oscc' for South Ops. 

        Optional Arguments: 
        
        1) level (Integer) - Default = 700. This is the level in millibars or hectopascals at which the user wishes to examine. 
                             700 means 700mb or 700hPa. Here are the following options: 850, 700, 500, 300, 250, 200. 

        2) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                            and passing the data in or if the function needs to download the data. A value of False means the data
                            is downloaded inside of the function while a value of True means the user is downloading the data outside
                            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                            things, it is recommended to set this value to True and download the data outside of the function and pass
                            it in so that the amount of data requests on the host servers can be minimized. 

        3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                        in the dataset. If the user wishes to download the data inside of the function, this value is None. 

        4) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        5) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        6) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                     

        7) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

        8) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        9) reference_system (String) - Default = 'States Only'. The georgraphical reference system with respect to the borders on the map. If the user
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
                               

        10) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        11) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        12) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        13) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        14) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        15) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        16) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        17) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

        18) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

        19) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

        20) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

        21) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

        22) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

        23) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

        24) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

        25) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        26) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        27) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        28) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        29) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        30) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        31) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'.    

        32) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        33) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        34) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        35) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        36) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        37) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        38) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                          This is a feature of matplotlib, as per their definition, the shrink is:
                                          "Fraction by which to multiply the size of the colorbar." 
                                          This should only be changed if the user wishes to make a custom plot. 
                                          Preset values are called from the settings module for each region. 

        39) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                 Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                 when making a custom plot. 

        40) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

        41) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        42) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.


        Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level

        '''
    
        data=data
        level=level
        ds=ds
        western_bound=western_bound
        eastern_bound=eastern_bound 
        southern_bound=southern_bound
        northern_bound=northern_bound
        show_rivers=show_rivers
        reference_system=reference_system
        state_border_linewidth=state_border_linewidth
        county_border_linewidth=county_border_linewidth
        gacc_border_linewidth=gacc_border_linewidth
        psa_border_linewidth=psa_border_linewidth 
        cwa_border_linewidth=cwa_border_linewidth
        nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
        nws_public_zones_linewidth=nws_public_zones_linewidth 
        state_border_linestyle=state_border_linestyle
        county_border_linestyle=county_border_linestyle
        gacc_border_linestyle=gacc_border_linestyle
        psa_border_linestyle=psa_border_linestyle 
        cwa_border_linestyle=cwa_border_linestyle
        nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
        nws_public_zones_linestyle=nws_public_zones_linestyle
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")

        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            mapcrs = ccrs.LambertConformal()
        else:
            mapcrs = ccrs.PlateCarree()
    
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
    
        str_level = f"{level} MB"
    
        if level == 850:
            hgt_levels = np.arange(96, 180, 4)
        if level == 700:
            hgt_levels = np.arange(240, 340, 4)
        if level == 300:
            hgt_levels = np.arange(840, 1020, 10)
        if level == 250:
            hgt_levels = np.arange(900, 1140, 10)
        if level == 200:
            hgt_levels = np.arange(1000, 1280, 10)

        rh_levels = np.arange(0, 101, 1)
        ticks = rh_levels[::5]

        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america' or region == 'conus' or region == 'CONUS' or region == 'CONUS & South Canada & North Mexico':

            rh_low_levels = [25]
            rh_high_levels = [75]
            
        else:

            rh_low_levels = np.arange(0, 50, 10)
            rh_high_levels = np.arange(55, 110, 10)            
    
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
            decimate = 20
            step = 1
            
            if level == 850:
                level_idx = 6
            if level == 700:
                level_idx = 12
            if level == 500:
                level_idx = 20
            if level == 300:
                level_idx = 28
            if level == 250:
                level_idx = 30
            if level == 200:
                level_idx = 32
        
        if model == 'CMCENS' or model == 'GEFS0p50':
            decimate = 10
            step = 1
    
            if level == 850:
                level_idx = 2
            if level == 700:
                level_idx = 3
            if level == 500:
                level_idx = 4
            if level == 300:
                level_idx = 6
            if level == 250:
                level_idx = 7
            if level == 200:
                level_idx = 8
            
        if model == 'GFS0p25' or model == 'GFS0p25_1h':
            decimate = 10
            step = 2
            
            if level == 850:
                level_idx = 5
            if level == 700:
                level_idx = 8
            if level == 500:
                level_idx = 12
            if level == 300:
                level_idx = 16
            if level == 250:
                level_idx = 17
            if level == 200:
                level_idx = 18
            
        if model == 'GFS0p50':
            decimate = 10
            step = 2
            
            if level == 850:
                level_idx = 6
            if level == 700:
                level_idx = 12
            if level == 500:
                level_idx = 20
            if level == 300:
                level_idx = 28
            if level == 250:
                level_idx = 30
            if level == 200:
                level_idx = 32
        
        if model == 'GFS1p00':
            decimate = 10
            step = 2
    
            if level == 850:
                level_idx = 5
            if level == 700:
                level_idx = 8
            if level == 500:
                level_idx = 12
            if level == 300:
                level_idx = 16
            if level == 250:
                level_idx = 17
            if level == 200:
                level_idx = 18
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
            wb=western_bound
            eb=eastern_bound
            sb=southern_bound
            nb=northern_bound
            x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
        else:
            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
            sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)
        
        if data == False:
            if model == 'RAP' or model == 'RAP 32':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
            else:
                ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
                
        if data == True:
            ds = ds
    
    
        cmap = colormaps.relative_humidity_colormap()
    
        end = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()
    
    
        path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, 'Height RH Wind', str_level)
    
        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass

        for t in range(0, end, step):
        
            fname = f"Image_{t}.png"
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            model = model.upper()
            plt.title(f"{model} {str_level} GPH [DM]/RH [%]/WIND [KTS]", fontsize=9, fontweight='bold', loc='left')
            plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props, zorder=11)
            
            lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
            
            stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                             transform=ccrs.PlateCarree(), zorder=3, fontsize=5, clip_on=True)
    
    
            if model == 'CMCENS' or model == 'GEFS0P50':
    
                stn.plot_barb((ds['ugrdprs'][0, t, level_idx, ::decimate, ::decimate] * 1.94384), (ds['vgrdprs'][0, t, level_idx, ::decimate, ::decimate] * 1.94384), color='black', alpha=1, zorder=3, linewidth=0.25)
    
                if level == 500:
                    c_neg = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=np.arange(440, 540, 4), colors='black', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                    c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=[540], colors='black', zorder=2, transform=datacrs, linewidths=1)
                    c_pos = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=np.arange(544, 624, 4), colors='black', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                    ax.clabel(c_neg, levels=np.arange(440, 540, 4), inline=True, fontsize=8, rightside_up=True)
                    ax.clabel(c, levels=[540], inline=True, fontsize=8, rightside_up=True)
                    ax.clabel(c_pos, levels=np.arange(544, 624, 4), inline=True, fontsize=8, rightside_up=True)
    
                else:                
                    c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][0, t, level_idx, :, :]/10), levels=hgt_levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                    ax.clabel(c, levels=hgt_levels, inline=True, fontsize=8, rightside_up=True)

                c_rh_below = ax.contour(ds['lon'], ds['lat'], ds['rhprs'][0, t, level_idx, :, :], colors='darkred', transform=datacrs, levels=rh_low_levels, linewidths=0.5, linestyles='--')
                ax.clabel(c_rh_below, levels=rh_low_levels, inline=True, fontsize=8, rightside_up=True)

                c_rh_0 = ax.contour(ds['lon'], ds['lat'], ds['rhprs'][0, t, level_idx, :, :], colors='dimgrey', transform=datacrs, levels=[50], linewidths=0.5, linestyles='--')
                ax.clabel(c_rh_0, levels=[50], inline=True, fontsize=8, rightside_up=True)

                c_rh_above = ax.contour(ds['lon'], ds['lat'], ds['rhprs'][0, t, level_idx, :, :], colors='darkblue', transform=datacrs, levels=rh_high_levels, linewidths=0.5, linestyles='--')
                ax.clabel(c_rh_above, levels=rh_high_levels, inline=True, fontsize=8, rightside_up=True)
                    
                cs = ax.contourf(ds['lon'], ds['lat'], ds['rhprs'][0, t, level_idx, :, :], cmap=cmap, transform=datacrs, levels=rh_levels, alpha=0.35)
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
    
            else:
                
                stn.plot_barb((ds['ugrdprs'][t, level_idx, ::decimate, ::decimate] * 1.94384), (ds['vgrdprs'][t, level_idx, ::decimate, ::decimate] * 1.94384), color='black', alpha=1, zorder=3, linewidth=0.25)
    
                if level == 500:
                    c_neg = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=np.arange(440, 540, 4), colors='black', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                    c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=[540], colors='black', zorder=2, transform=datacrs, linewidths=1)
                    c_pos = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=np.arange(544, 624, 4), colors='black', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
                    ax.clabel(c_neg, levels=np.arange(440, 540, 4), inline=True, fontsize=8, rightside_up=True)
                    ax.clabel(c, levels=[540], inline=True, fontsize=8, rightside_up=True)
                    ax.clabel(c_pos, levels=np.arange(544, 624, 4), inline=True, fontsize=8, rightside_up=True)
    
                else:
                    c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=hgt_levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                    ax.clabel(c, levels=hgt_levels, inline=True, fontsize=8, rightside_up=True)

                c_rh_below = ax.contour(ds['lon'], ds['lat'], ds['rhprs'][t, level_idx, :, :], colors='darkred', transform=datacrs, levels=rh_low_levels, linewidths=0.5, linestyles='--')
                ax.clabel(c_rh_below, levels=rh_low_levels, inline=True, fontsize=8, rightside_up=True)

                c_rh_0 = ax.contour(ds['lon'], ds['lat'], ds['rhprs'][t, level_idx, :, :], colors='dimgrey', transform=datacrs, levels=[0], linewidths=0.5, linestyles='--')
                ax.clabel(c_rh_0, levels=[0], inline=True, fontsize=8, rightside_up=True)

                c_rh_above = ax.contour(ds['lon'], ds['lat'], ds['rhprs'][t, level_idx, :, :], colors='darkblue', transform=datacrs, levels=rh_high_levels, linewidths=0.5, linestyles='--')
                ax.clabel(c_rh_above, levels=rh_high_levels, inline=True, fontsize=8, rightside_up=True)
                
                cs = ax.contourf(ds['lon'], ds['lat'], ds['rhprs'][t, level_idx, :, :], cmap=cmap, transform=datacrs, levels=rh_levels, alpha=0.35)
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
        print(f"Saved forecast graphics to {path_print}.")
            

class critical_firewx_conditions:

    r'''
    This class hosts the functions plotting critical fire weather forecasts. 

    '''

    def plot_favorable_firewx_conditions(model, region, low_rh_threshold=15, high_wind_threshold=25, use_wind_gust=False, temperature_threshold=None, data=False, ds=None, ds_list=None, u=None, v=None, gusts=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=20, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

        r'''
        This function plots the Favorable Fire Weather Forecast. 

        Required Arguments: 
        
        1) model (String) - This is the model the user must select. 
                               
           Here are the choices: 
           1) GFS0p25 - GFS 0.25x0.25 degree
           2) GFS0p50 - GFS 0.5x0.5 degree
           3) GFS1p00 - GFS 1.0x1.0 degree
           4) GEFS0p50 - GEFS 0.5x0.5 degree
           5) CMCENS - Canadian Ensemble
           6) NAM - North American Model
           7) NA NAM - 32km North American Model - Full North America
           8) RAP - Rapid Refresh Model
           9) RAP 32 - 32km Rapid Refresh Model - Full North America
           10) GEFS0p25 ENS MEAN - GEFS 0.25x0.25 degree Ensemble Mean

        2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                             To look at any state use the 2-letter abbreviation for the state in either all capitals
                             or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                             CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                             North America use either: NA, na, North America or north america. If the user wishes to use custom
                             boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                             the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                             'oscc' for South Ops. 

        Optional Arguments: 
        
        1) low_rh_threshold (Integer) - Default = 15. The threshold for the contour line that defines what extremely low relative humidity is.

        2) high_wind_threshold (Integer) - Default = 25. The threshold for the contour line that defines what high winds are.

        3) use_wind_gust (Boolean) - Default = False. When set to False, the red shading is determined by the intersection of either the 
                                    RH & Sustained Wind Speed or RH & Temperature & Sustained Wind Speed. When set to True, the red shading
                                    is determined by the intersection of RH & Wind Gust or RH & Temperature & Wind Gust. 

        4) temperature_threshold (Integer) - Default = None. This is to be used if the user wishes to add temperature as a factor to what 
                                             defines favorable fire weather conditions. When set to None, only RH & Wind Speed/Gust are taken 
                                             into account. When set to an integer value, the temperature will also be taken into account. 

        5) data (Boolean) - Default = False. This tells the function if the user is downloading the data outside of the function
                            and passing the data in or if the function needs to download the data. A value of False means the data
                            is downloaded inside of the function while a value of True means the user is downloading the data outside
                            of the function and passing it in. For users who intend to make a lot of graphics for a lot of different 
                            things, it is recommended to set this value to True and download the data outside of the function and pass
                            it in so that the amount of data requests on the host servers can be minimized. 

         

        3) ds (Array) - Default = None. This is the dataset the user passes in if the user downloads the data outside of the function and passes
                        in the dataset. If the user wishes to download the data inside of the function, this value is None. When downloading data
                        outside of the function and passing in the data, this is for any model that is NOT the 'GEFS0p25 ENS MEAN'. 

        4) ds_list (List) - Default = None. This is the list of datasets the user passes in if the user downloads the data outside of the function
                            and passes in the list of datasets. This is used when the user wishes to plot the 'GEFS0p25 ENS MEAN' since that data
                            needs to be downloaded via HTTPS as it is unavailable on the OpenDAP. If the user wishes to download the data inside of the function, this value is None.

        5) u (List) - Default = None. This is the list of u-wind datasets the user passes in if the user downloads the data outside of the function
                            and passes in the list of datasets. This is used when the user wishes to plot the 'GEFS0p25 ENS MEAN' since that data
                            needs to be downloaded via HTTPS as it is unavailable on the OpenDAP. If the user wishes to download the data inside of the function, this value is None.

        6) v (List) - Default = None. This is the list of v-wind datasets the user passes in if the user downloads the data outside of the function
                            and passes in the list of datasets. This is used when the user wishes to plot the 'GEFS0p25 ENS MEAN' since that data
                            needs to be downloaded via HTTPS as it is unavailable on the OpenDAP. If the user wishes to download the data inside of the function, this value is None.

        7) gusts (List) - Default = None. This is the list of wind gust datasets the user passes in if the user downloads the data outside of the function
                            and passes in the list of datasets. This is used when the user wishes to plot the 'GEFS0p25 ENS MEAN' since that data
                            needs to be downloaded via HTTPS as it is unavailable on the OpenDAP. If the user wishes to download the data inside of the function, this value is None.

        8) western_bound (Integer) - The western boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        9) eastern_bound (Integer) - The eastern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 


        10) southern_bound (Integer) - The southern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 
                                     

        11) northern_bound (Integer) - The northern boundary of the plot. This is only required when the user wishes to make a plot with
                                     custom boundaries. This should be set to None if the user wishes to use a pre-defined region. 

        12) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.

        13) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
                               

        14) show_state_borders (Boolean) - If set to True, state borders will display. If set to False, state borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide state borders. 

        15) show_county_borders (Boolean) - If set to True, county borders will display. If set to False, county borders will not display. 
            Default setting is False. Users should change this value to False if they wish to hide county borders. 

        16) show_gacc_borders (Boolean) - If set to True, GACC (Geographic Area Coordination Center) borders will display. If set to False, GACC borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display GACC borders. 

        17) show_psa_borders (Boolean) - If set to True, PSA (Predictive Services Area) borders will display. If set to False, PSA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display PSA borders.

        18) show_cwa_borders (Boolean) - If set to True, CWA borders will display. If set to False, CWA borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display CWA borders.

        19) show_nws_firewx_zones (Boolean) - If set to True, NWS FWZ borders will display. If set to False, NWS FWZ borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS FWZ borders.

        20) show_nws_public_zones (Boolean) - If set to True, NWS Public Zone borders will display. If set to False, NWS Public Zone borders will not display. 
            Default setting is False. Users should change this value to True if they wish to display NWS Public Zone borders.

        21) state_border_linewidth (Integer or Float) - Linewidth (thickness) of the state borders. Default setting is 1. 

        22) province_border_linewidth (Integer or Float) - Linewidth (thickness) of the Canadian province borders. Default setting is 1. 

        23) county_border_linewidth (Integer or Float) - Linewidth (thickness) of the county borders. Default setting is 0.25. 

        24) gacc_border_linewidth (Integer or Float) - Linewidth (thickness) of the GACC borders. Default setting is 1. 

        25) psa_border_linewidth (Integer or Float) - Linewidth (thickness) of the PSA borders. Default setting is 0.25. 

        26) cwa_border_linewidth (Integer or Float) - Linewidth (thickness) of the NWS CWA borders. Default setting is 1. 

        27) nws_firewx_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS FWZ borders. Default setting is 0.25. 

        28) nws_public_zones_linewidth (Integer or Float) - Linewidth (thickness) of the NWS Public Zone borders. Default setting is 0.25. 

        29) state_border_linestyle (String) - Linestyle of the state borders. Default is a solid line. 
            To change to a dashed line, users should set state_border_linestyle='--'. 

        30) county_border_linestyle (String) - Linestyle of the county borders. Default is a solid line. 
            To change to a dashed line, users should set county_border_linestyle='--'. 

        31) gacc_border_linestyle (String) - Linestyle of the GACC borders. Default is a solid line. 
            To change to a dashed line, users should set gacc_border_linestyle='--'. 

        32) psa_border_linestyle (String) - Linestyle of the PSA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        33) cwa_border_linestyle (String) - Linestyle of the CWA borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        34) nws_firewx_zones_linestyle (String) - Linestyle of the NWS FWZ borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'. 

        35) nws_public_zones_linestyle (String) - Linestyle of the NWS Public Zone borders. Default is a solid line. 
            To change to a dashed line, users should set psa_border_linestyle='--'.    

        36) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 

        37) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 

        38) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.

        39) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.

        40) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.

        41) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.

        42) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                          This is a feature of matplotlib, as per their definition, the shrink is:
                                          "Fraction by which to multiply the size of the colorbar." 
                                          This should only be changed if the user wishes to make a custom plot. 
                                          Preset values are called from the settings module for each region. 

        43) decimate (Integer) - Default = 20. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                 Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                 when making a custom plot. 

        44) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 

        45) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 

        46) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.

        47) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.

        48) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 


        Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level


        '''
    
        data=data
        ds=ds
        western_bound=western_bound
        eastern_bound=eastern_bound 
        southern_bound=southern_bound
        northern_bound=northern_bound
        show_rivers=show_rivers
        reference_system=reference_system
        state_border_linewidth=state_border_linewidth
        county_border_linewidth=county_border_linewidth
        gacc_border_linewidth=gacc_border_linewidth
        psa_border_linewidth=psa_border_linewidth 
        cwa_border_linewidth=cwa_border_linewidth
        nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
        nws_public_zones_linewidth=nws_public_zones_linewidth 
        state_border_linestyle=state_border_linestyle
        county_border_linestyle=county_border_linestyle
        gacc_border_linestyle=gacc_border_linestyle
        psa_border_linestyle=psa_border_linestyle 
        cwa_border_linestyle=cwa_border_linestyle
        nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
        nws_public_zones_linestyle=nws_public_zones_linestyle
        x1=x1 
        y1=y1
        x2=x2
        y2=y2 
        x3=x3
        y3=y3 
        shrink=shrink
        sample_point_fontsize=sample_point_fontsize
        x=x 
        y=y
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        levels = np.arange(0, 101, 1)
        ticks = levels[::5]
    
        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            mapcrs = ccrs.LambertConformal()
        else:
            mapcrs = ccrs.PlateCarree()
    
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
    
        str_level = f"SURFACE"
    
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
            step = 1
        
        if model == 'CMCENS' or model == 'GEFS0p50':
            step = 1
            
        if model == 'GFS0p25' or model == 'GFS0p25_1h':
            step = 2
            
        if model == 'GFS0p50':
            step = 2
        
        if model == 'GFS1p00':
            step = 2
    
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
            wb=western_bound
            eb=eastern_bound
            sb=southern_bound
            nb=northern_bound
            x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
        else:
            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
            sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)
    
            if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
                
                if region == 'conus' or region == 'North America' or region == 'north america' or region == 'NA' or region == 'na':
                    decimate = decimate * 2
                else:
                    decimate = decimate + 1
                    
            elif model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
                if region == 'conus' or region == 'North America' or region == 'north america' or region == 'NA' or region == 'na':
                    decimate = decimate * 2
                else:
                    decimate = decimate + 2
            else:
                decimate = decimate
        
        if data == False and model != 'GEFS0p25 ENS MEAN':
            if model == 'RAP' or model == 'RAP 32':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
            else:
                ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
    
        if data == False and model == 'GEFS0p25 ENS MEAN':
            ds_list, u, v, gusts = model_data.get_nomads_model_data_via_https(model, region, 'heightAboveGround', wb, eb, sb, nb, get_u_and_v_wind_components=True, add_wind_gusts=True)
            
        if data == True and model != 'GEFS0p25 ENS MEAN':
            ds = ds
    
        if data == True and model == 'GEFS0p25 ENS MEAN':
            ds_list = ds_list 
            u = u
            v = v
            gusts = gusts
    
    
        cmap = colormaps.red_flag_warning_criteria_colormap()
    
        if temperature_threshold == None:
    
            if use_wind_gust == False:
                path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, f"Favorable FireWx RH Less Than {low_rh_threshold} & Sustained Winds Greater Than {high_wind_threshold}", str_level)
            
                for file in os.listdir(f"{path}"):
                    try:
                        os.remove(f"{path}/{file}")
                    except Exception as e:
                        pass
    
            if use_wind_gust == True:
                path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, f"Favorable FireWx RH Less Than {low_rh_threshold} & Wind Gusts Greater Than {high_wind_threshold}", str_level)
            
                for file in os.listdir(f"{path}"):
                    try:
                        os.remove(f"{path}/{file}")
                    except Exception as e:
                        pass
    
        if temperature_threshold != None:
    
            if use_wind_gust == False:
                path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, f"Favorable FireWx Temperature Greater Than {temperature_threshold} & RH Less Than {low_rh_threshold} & Sustained Winds Greater Than {high_wind_threshold}", str_level)
            
                for file in os.listdir(f"{path}"):
                    try:
                        os.remove(f"{path}/{file}")
                    except Exception as e:
                        pass
    
            if use_wind_gust == True:
                path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, f"Favorable FireWx Temperature Greater Than {temperature_threshold} & RH Less Than {low_rh_threshold} & Wind Gusts Greater Than {high_wind_threshold}", str_level)
            
                for file in os.listdir(f"{path}"):
                    try:
                        os.remove(f"{path}/{file}")
                    except Exception as e:
                        pass

        if model != 'GEFS0p25 ENS MEAN':
    
            end1 = (int(round((len(ds['time']) - 1)/6, 0)) - 1)
            end2 = len(ds['time']) - 1
            time = ds['time']
            times = time.to_pandas()
    
            if temperature_threshold == None:
    
                if use_wind_gust == False:
                    ds['wind_speed'] = np.hypot(ds['ugrd10m'], ds['vgrd10m']) * 2.23694
                if use_wind_gust == True:
                    ds['wind_speed'] = ds['gustsfc'] * 2.23694
        
                ds['u'] = ds['ugrd10m'] * 2.23694
                ds['v'] = ds['vgrd10m'] * 2.23694
                
                mask = (ds['rh2m'] <= low_rh_threshold) & (ds['wind_speed'] >= high_wind_threshold)
            
                for t in range(0, end1, 1):
                
                    fname = f"Image_{t}.png"
                
                    fig = plt.figure(figsize=(12, 12))
                    fig.set_facecolor('aliceblue')
                    
                    ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                    ax.set_extent([wb, eb, sb, nb], datacrs)
                    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
                    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
                    ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
                    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
                    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
                    ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
                    if show_rivers == True:
                        ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
                    else:
                        pass
                
                    if show_gacc_borders == True:
                        ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                    else:
                        pass
                    if show_psa_borders == True:
                        ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_county_borders == True:
                        ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_state_borders == True:
                        ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                    else:
                        pass
                    if show_cwa_borders == True:
                        ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_nws_firewx_zones == True:
                        ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                    else:
                        pass
                    if show_nws_public_zones == True:
                        ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                    else:
                        pass
            
                    model = model.upper()
                    
                    if use_wind_gust == False:
                        plt.title(f"{model} FAVORABLE FIREWX CONDITIONS (SHADED RED)\n[RH <= {low_rh_threshold} [%] & SUSTAINED WIND SPEED >= {high_wind_threshold} [MPH]]", fontsize=9, fontweight='bold', loc='left')
                        ax.text(x, y, f"KEY: RH = GREEN | SUSTAINED WIND = BARBS & CYAN", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
                    if use_wind_gust == True:
                        plt.title(f"{model} FAVORABLE FIREWX CONDITIONS (SHADED RED)\n[RH <= {low_rh_threshold} [%] & WIND GUST >= {high_wind_threshold} [MPH]]", fontsize=9, fontweight='bold', loc='left')
                        ax.text(x, y, f"KEY: RH = GREEN | SUSTAINED WIND = BARBS | WIND GUSTS = CYAN", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
                        
                    plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                    ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
                    ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
                    ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
                    
                    lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
        
                    numbers = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                                     transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
            
                    barbs = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                                     transform=ccrs.PlateCarree(), zorder=3, fontsize=8, clip_on=True)
            
                    if model == 'CMCENS' or model == 'GEFS0P50':
            
                        rh = ds['rh2m'][0, t, :, :]
        
                        wind = ds['wind_speed'][0, t, :, :]
            
                        rh = rh[::decimate, ::decimate].to_numpy().flatten()
        
                        wind = wind[::decimate, ::decimate].to_numpy().flatten()
        
                        barbs.plot_barb(ds['u'][0, t, ::decimate, ::decimate], ds['v'][0, t, ::decimate, ::decimate], color='black', alpha=1, zorder=3, linewidth=0.5)
                
                        numbers.plot_parameter('SW', rh, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                        numbers.plot_parameter('NW', wind, color='cyan', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                        try:
                            ax.pcolormesh(mask['lon'], mask['lat'], mask[0, t, :, :], transform=datacrs, cmap=cmap, zorder=1, alpha=0.5)
                        except Exception as e:
                            pass
            
                        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                        plt.close(fig)
                        if mapcrs == datacrs:
                            tim.sleep(10)
            
            
                    else:
                        
                        rh = ds['rh2m'][t, :, :]
        
                        wind = ds['wind_speed'][t, :, :]
            
                        rh = rh[::decimate, ::decimate].to_numpy().flatten()
        
                        wind = wind[::decimate, ::decimate].to_numpy().flatten()
        
                        barbs.plot_barb(ds['u'][t, ::decimate, ::decimate], ds['v'][t, ::decimate, ::decimate], color='black', alpha=1, zorder=3, linewidth=0.5)
                
                        numbers.plot_parameter('SW', rh, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                        numbers.plot_parameter('NW', wind, color='cyan', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
            
                        try:
                            ax.pcolormesh(mask['lon'], mask['lat'], mask[t, :, :], transform=datacrs, cmap=cmap, zorder=1, alpha=0.5)
                        except Exception as e:
                            pass
                
                        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                        plt.close(fig)
                        if mapcrs == datacrs:
                            tim.sleep(10)
            
                for t in range(end1, end2, step):
                
                    fname = f"Image_{t}.png"
                
                    fig = plt.figure(figsize=(12, 12))
                    fig.set_facecolor('aliceblue')
                    
                    ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                    ax.set_extent([wb, eb, sb, nb], datacrs)
                    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
                    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
                    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
                    ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
                    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
                    ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
                    if show_rivers == True:
                        ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
                    else:
                        pass
                
                    if show_gacc_borders == True:
                        ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                    else:
                        pass
                    if show_psa_borders == True:
                        ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_county_borders == True:
                        ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_state_borders == True:
                        ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                    else:
                        pass
                    if show_cwa_borders == True:
                        ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_nws_firewx_zones == True:
                        ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                    else:
                        pass
                    if show_nws_public_zones == True:
                        ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                    else:
                        pass
            
                    model = model.upper()
                    
                    if use_wind_gust == False:
                        plt.title(f"{model} FAVORABLE FIREWX CONDITIONS (SHADED RED)\n[RH <= {low_rh_threshold} [%] & SUSTAINED WIND SPEED >= {high_wind_threshold} [MPH]]", fontsize=9, fontweight='bold', loc='left')
                        ax.text(x, y, f"KEY: RH = GREEN | SUSTAINED WIND = BARBS & CYAN", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
                    if use_wind_gust == True:
                        plt.title(f"{model} FAVORABLE FIREWX CONDITIONS (SHADED RED)\n[RH <= {low_rh_threshold} [%] & WIND GUST >= {high_wind_threshold} [MPH]]", fontsize=9, fontweight='bold', loc='left')
                        ax.text(x, y, f"KEY: RH = GREEN | SUSTAINED WIND = BARBS | WIND GUSTS = CYAN", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11) 
                        
                    plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                    ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
                    ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
                    ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
                    
                    lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
            
                    numbers = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                                     transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
            
                    barbs = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                                     transform=ccrs.PlateCarree(), zorder=3, fontsize=8, clip_on=True)
            
                    if model == 'CMCENS' or model == 'GEFS0P50':
            
                        rh = ds['rh2m'][0, t, :, :]
        
                        wind = ds['wind_speed'][0, t, :, :]
            
                        rh = rh[::decimate, ::decimate].to_numpy().flatten()
        
                        wind = wind[::decimate, ::decimate].to_numpy().flatten()
        
                        barbs.plot_barb(ds['u'][0, t, ::decimate, ::decimate], ds['v'][0, t, ::decimate, ::decimate], color='black', alpha=1, zorder=3, linewidth=0.5)
                
                        numbers.plot_parameter('SW', rh, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                        numbers.plot_parameter('NW', wind, color='cyan', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
            
                        try:
                            ax.pcolormesh(mask['lon'], mask['lat'], mask[0, t, :, :], transform=datacrs, cmap=cmap, zorder=1, alpha=0.5)
                        except Exception as e:
                            pass
            
                        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                        plt.close(fig)
                        if mapcrs == datacrs:
                            tim.sleep(10)
            
            
                    else:
                        
                        rh = ds['rh2m'][t, :, :]
        
                        wind = ds['wind_speed'][t, :, :]
            
                        rh = rh[::decimate, ::decimate].to_numpy().flatten()
        
                        wind = wind[::decimate, ::decimate].to_numpy().flatten()
        
                        barbs.plot_barb(ds['u'][t, ::decimate, ::decimate], ds['v'][t, ::decimate, ::decimate], color='black', alpha=1, zorder=3, linewidth=0.5)
                
                        numbers.plot_parameter('SW', rh, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                        numbers.plot_parameter('NW', wind, color='cyan', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
            
                        try:
                            ax.pcolormesh(mask['lon'], mask['lat'], mask[t, :, :], transform=datacrs, cmap=cmap, zorder=1, alpha=0.5)
                        except Exception as e:
                            pass
                
                        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                        plt.close(fig)
                        if mapcrs == datacrs:
                            tim.sleep(10)
    
            if temperature_threshold != None:
        
                if use_wind_gust == False:
                    ds['wind_speed'] = np.hypot(ds['ugrd10m'], ds['vgrd10m']) * 2.23694
                if use_wind_gust == True:
                    ds['wind_speed'] = ds['gustsfc'] * 2.23694
        
                ds['u'] = ds['ugrd10m'] * 2.23694
                ds['v'] = ds['vgrd10m'] * 2.23694
        
                ds['temperature'] = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(ds['tmp2m'])
                
                mask = (ds['rh2m'] <= low_rh_threshold) & (ds['wind_speed'] >= high_wind_threshold) & (ds['temperature'] >= temperature_threshold)
            
                for t in range(0, end1, 1):
                
                    fname = f"Image_{t}.png"
                
                    fig = plt.figure(figsize=(12, 12))
                    fig.set_facecolor('aliceblue')
                    
                    ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                    ax.set_extent([wb, eb, sb, nb], datacrs)
                    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
                    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
                    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
                    ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
                    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
                    ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
                    if show_rivers == True:
                        ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
                    else:
                        pass
                
                    if show_gacc_borders == True:
                        ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                    else:
                        pass
                    if show_psa_borders == True:
                        ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_county_borders == True:
                        ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_state_borders == True:
                        ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                    else:
                        pass
                    if show_cwa_borders == True:
                        ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_nws_firewx_zones == True:
                        ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                    else:
                        pass
                    if show_nws_public_zones == True:
                        ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                    else:
                        pass
            
                    model = model.upper()
                    
                    if use_wind_gust == False:
                        plt.title(f"{model} FAVORABLE FIREWX CONDITIONS (SHADED RED)\n[T >= {temperature_threshold} [°F] & RH <= {low_rh_threshold} [%] & SUSTAINED WIND SPEED >= {high_wind_threshold} [MPH]]", fontsize=9, fontweight='bold', loc='left')
                        ax.text(x, y, f"KEY: T = ORANGE | RH = GREEN | SUSTAINED WIND = BARBS & CYAN", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
        
                    if use_wind_gust == True:
                        plt.title(f"{model} FAVORABLE FIREWX CONDITIONS (SHADED RED)\n[T >= {temperature_threshold} [°F] & RH <= {low_rh_threshold} [%] & WIND GUST >= {high_wind_threshold} [MPH]]", fontsize=9, fontweight='bold', loc='left')
                        ax.text(x, y, f"KEY: T = ORANGE | RH = GREEN | SUSTAINED WIND = BARBS | WIND GUSTS = CYAN", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
        
                    plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                    ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
                    ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
                    ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
                    
                    lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
        
                    numbers = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                                     transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
            
                    barbs = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                                     transform=ccrs.PlateCarree(), zorder=3, fontsize=8, clip_on=True)
            
                    if model == 'CMCENS' or model == 'GEFS0P50':
            
                        rh = ds['rh2m'][0, t, :, :]
        
                        wind = ds['wind_speed'][0, t, :, :]
        
                        temp = ds['temperature'][0, t, :, :]
            
                        rh = rh[::decimate, ::decimate].to_numpy().flatten()
        
                        wind = wind[::decimate, ::decimate].to_numpy().flatten()
        
                        temp = temp[::decimate, ::decimate].to_numpy().flatten()
        
                        barbs.plot_barb(ds['u'][0, t, ::decimate, ::decimate], ds['v'][0, t, ::decimate, ::decimate], color='black', alpha=1, zorder=3, linewidth=0.5)
                
                        numbers.plot_parameter('SW', rh, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                        numbers.plot_parameter('NW', temp, color='darkorange', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                        numbers.plot_parameter('SE', wind, color='cyan', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                        try:
                            ax.pcolormesh(mask['lon'], mask['lat'], mask[0, t, :, :], transform=datacrs, cmap=cmap, zorder=1, alpha=0.5)
                        except Exception as e:
                            pass
            
                        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                        plt.close(fig)
                        if mapcrs == datacrs:
                            tim.sleep(10)
            
            
                    else:
                        
                        rh = ds['rh2m'][t, :, :]
        
                        wind = ds['wind_speed'][t, :, :]
        
                        temp = ds['temperature'][t, :, :]
            
                        rh = rh[::decimate, ::decimate].to_numpy().flatten()
        
                        wind = wind[::decimate, ::decimate].to_numpy().flatten()
        
                        temp = temp[::decimate, ::decimate].to_numpy().flatten()
        
                        barbs.plot_barb(ds['u'][t, ::decimate, ::decimate], ds['v'][t, ::decimate, ::decimate], color='black', alpha=1, zorder=3, linewidth=0.5)
                
                        numbers.plot_parameter('SW', rh, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                        numbers.plot_parameter('NW', temp, color='darkorange', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                        numbers.plot_parameter('SE', wind, color='cyan', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
            
                        try:
                            ax.pcolormesh(mask['lon'], mask['lat'], mask[t, :, :], transform=datacrs, cmap=cmap, zorder=1, alpha=0.5)
                        except Exception as e:
                            pass
                
                        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                        plt.close(fig)
                        if mapcrs == datacrs:
                            tim.sleep(10)
            
                for t in range(end1, end2, step):
                
                    fname = f"Image_{t}.png"
                
                    fig = plt.figure(figsize=(12, 12))
                    fig.set_facecolor('aliceblue')
                    
                    ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                    ax.set_extent([wb, eb, sb, nb], datacrs)
                    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
                    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
                    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
                    ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
                    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
                    ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
                    if show_rivers == True:
                        ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
                    else:
                        pass
                
                    if show_gacc_borders == True:
                        ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                    else:
                        pass
                    if show_psa_borders == True:
                        ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_county_borders == True:
                        ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_state_borders == True:
                        ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                    else:
                        pass
                    if show_cwa_borders == True:
                        ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_nws_firewx_zones == True:
                        ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                    else:
                        pass
                    if show_nws_public_zones == True:
                        ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                    else:
                        pass
            
                    model = model.upper()
                    
                    if use_wind_gust == False:
                        plt.title(f"{model} FAVORABLE FIREWX CONDITIONS (SHADED RED)\n[T >= {temperature_threshold} [°F] & RH <= {low_rh_threshold} [%] & SUSTAINED WIND SPEED >= {high_wind_threshold} [MPH]]", fontsize=9, fontweight='bold', loc='left')
                        ax.text(x, y, f"KEY: T = ORANGE | RH = GREEN | SUSTAINED WIND = BARBS & CYAN", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
        
                    if use_wind_gust == True:
                        plt.title(f"{model} FAVORABLE FIREWX CONDITIONS (SHADED RED)\n[T >= {temperature_threshold} [°F] & RH <= {low_rh_threshold} [%] & WIND GUST >= {high_wind_threshold} [MPH]]", fontsize=9, fontweight='bold', loc='left')
                        ax.text(x, y, f"KEY: T = ORANGE | RH = GREEN | SUSTAINED WIND = BARBS | WIND GUSTS = CYAN", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
                        
                    plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                    ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
                    ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
                    ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
                    
                    lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
            
                    numbers = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                                     transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
            
                    barbs = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                                     transform=ccrs.PlateCarree(), zorder=3, fontsize=8, clip_on=True)
            
                    if model == 'CMCENS' or model == 'GEFS0P50':
            
                        rh = ds['rh2m'][0, t, :, :]
        
                        wind = ds['wind_speed'][0, t, :, :]
        
                        temp = ds['temperature'][0, t, :, :]
            
                        rh = rh[::decimate, ::decimate].to_numpy().flatten()
        
                        wind = wind[::decimate, ::decimate].to_numpy().flatten()
        
                        temp = temp[::decimate, ::decimate].to_numpy().flatten()
        
                        barbs.plot_barb(ds['u'][0, t, ::decimate, ::decimate], ds['v'][0, t, ::decimate, ::decimate], color='black', alpha=1, zorder=3, linewidth=0.5)
                
                        numbers.plot_parameter('SW', rh, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                        numbers.plot_parameter('NW', temp, color='darkorange', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                        numbers.plot_parameter('SE', wind, color='cyan', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
            
                        try:
                            ax.pcolormesh(mask['lon'], mask['lat'], mask[0, t, :, :], transform=datacrs, cmap=cmap, zorder=1, alpha=0.5)
                        except Exception as e:
                            pass
            
                        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                        plt.close(fig)
                        if mapcrs == datacrs:
                            tim.sleep(10)
            
            
                    else:
                        
                        rh = ds['rh2m'][t, :, :]
        
                        wind = ds['wind_speed'][t, :, :]
        
                        temp = ds['temperature'][t, :, :]
            
                        rh = rh[::decimate, ::decimate].to_numpy().flatten()
        
                        wind = wind[::decimate, ::decimate].to_numpy().flatten()
        
                        temp = temp[::decimate, ::decimate].to_numpy().flatten()
        
                        barbs.plot_barb(ds['u'][t, ::decimate, ::decimate], ds['v'][t, ::decimate, ::decimate], color='black', alpha=1, zorder=3, linewidth=0.5)
                
                        numbers.plot_parameter('SW', rh, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                        numbers.plot_parameter('NW', temp, color='darkorange', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                        numbers.plot_parameter('SE', wind, color='cyan', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
            
                        try:
                            ax.pcolormesh(mask['lon'], mask['lat'], mask[t, :, :], transform=datacrs, cmap=cmap, zorder=1, alpha=0.5)
                        except Exception as e:
                            pass
                
                        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                        plt.close(fig)
                        if mapcrs == datacrs:
                            tim.sleep(10)
    
        if model == 'GEFS0p25 ENS MEAN':
    
            if temperature_threshold == None:
    
                for i in range(0, (len(ds_list) - 1)):
                
                    if use_wind_gust == False:
                        wind_speed = np.hypot(u[i]['u10'], v[i]['v10']) * 2.23694
                    if use_wind_gust == True:
                        wind_speed = gusts[i] * 2.23694
    
                    time = ds_list[i]['valid_time']
                    init = ds_list[0]['time']
                    times = time.to_pandas()
                    times = pd.to_datetime(times)
                    inits = init.to_pandas()
                    inits = pd.to_datetime(inits)
        
                    u_wind = u[i]['u10'] * 2.23694
                    v_wind = v[i]['v10'] * 2.23694
                    rh = ds_list[i]['r2']
                
                    mask = (rh <= low_rh_threshold) & (wind_speed >= high_wind_threshold)
    
                    fname = f"Image_{i}.png"
                
                    fig = plt.figure(figsize=(12, 12))
                    fig.set_facecolor('aliceblue')
                    
                    ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                    ax.set_extent([wb, eb, sb, nb], datacrs)
                    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
                    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
                    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
                    ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
                    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
                    ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
                    if show_rivers == True:
                        ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
                    else:
                        pass
                
                    if show_gacc_borders == True:
                        ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                    else:
                        pass
                    if show_psa_borders == True:
                        ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_county_borders == True:
                        ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_state_borders == True:
                        ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                    else:
                        pass
                    if show_cwa_borders == True:
                        ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_nws_firewx_zones == True:
                        ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                    else:
                        pass
                    if show_nws_public_zones == True:
                        ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                    else:
                        pass
            
                    model = model.upper()
                    
                    if use_wind_gust == False:
                        plt.title(f"{model} FAVORABLE FIREWX CONDITIONS (SHADED RED)\n[RH <= {low_rh_threshold} [%] & SUSTAINED WIND SPEED >= {high_wind_threshold} [MPH]]", fontsize=9, fontweight='bold', loc='left')
                        ax.text(x, y, f"KEY: RH = GREEN | SUSTAINED WIND = BARBS & CYAN", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
                    if use_wind_gust == True:
                        plt.title(f"{model} FAVORABLE FIREWX CONDITIONS (SHADED RED)\n[RH <= {low_rh_threshold} [%] & WIND GUST >= {high_wind_threshold} [MPH]]", fontsize=9, fontweight='bold', loc='left')
                        ax.text(x, y, f"KEY: RH = GREEN | SUSTAINED WIND = BARBS | WIND GUSTS = CYAN", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
                        
                    plt.title("Forecast Valid: " +times.strftime('%a %d/%H UTC')+"\nInitialization: "+inits.strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                    ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
                    ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
                    ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
                    
                    lon_2d, lat_2d = np.meshgrid(ds_list[i]['longitude'], ds_list[i]['latitude'])
        
                    numbers = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                                     transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
            
                    barbs = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                                     transform=ccrs.PlateCarree(), zorder=3, fontsize=8, clip_on=True)
    
                        
        
                    rh = rh[::decimate, ::decimate].to_numpy().flatten()
    
                    wind_speed = wind_speed[::decimate, ::decimate].to_numpy().flatten()
    
                    barbs.plot_barb(u_wind[::decimate, ::decimate], v_wind[::decimate, ::decimate], color='black', alpha=1, zorder=3, linewidth=0.5)
            
                    numbers.plot_parameter('SW', rh, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
                    numbers.plot_parameter('SE', wind_speed, color='cyan', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                    try:
                        ax.pcolormesh(mask['longitude'], mask['latitude'], mask[:, :], transform=datacrs, cmap=cmap, zorder=1, alpha=0.5)
                    except Exception as e:
                        pass
            
                    fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                    plt.close(fig)
                    if mapcrs == datacrs:
                        tim.sleep(10)
    
            if temperature_threshold != None:
    
                for i in range(0, (len(ds_list) - 1)):
                
                    if use_wind_gust == False:
                        wind_speed = np.hypot(u[i]['u10'], v[i]['v10']) * 2.23694
                    if use_wind_gust == True:
                        wind_speed = gusts[i] * 2.23694
    
                    time = ds_list[i]['time']
                    init = ds_list[0]['time']
                    times = time.to_pandas()
                    times = pd.to_datetime(times)
                    inits = init.to_pandas()
                    inits = pd.to_datetime(inits)
    
                    tempK = ds_list[i]['t2m']
                    temp = unit_conversion.Temperature_Data_or_Dewpoint_Data_Kelvin_to_Fahrenheit(tempK)
        
                    u_wind = u[i]['u10'] * 2.23694
                    v_wind = v[i]['v10'] * 2.23694
                    rh = ds_list[i]['r2']
                
                    mask = (rh <= low_rh_threshold) & (wind_speed >= high_wind_threshold) & (temp >= temperature_threshold)
    
                    fname = f"Image_{i}.png"
                
                    fig = plt.figure(figsize=(12, 12))
                    fig.set_facecolor('aliceblue')
                    
                    ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
                    ax.set_extent([wb, eb, sb, nb], datacrs)
                    ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
                    ax.add_feature(cfeature.LAND, color='beige', zorder=1)
                    ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
                    ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
                    ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
                    ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
                    if show_rivers == True:
                        ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
                    else:
                        pass
                
                    if show_gacc_borders == True:
                        ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
                    else:
                        pass
                    if show_psa_borders == True:
                        ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_county_borders == True:
                        ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_state_borders == True:
                        ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
                    else:
                        pass
                    if show_cwa_borders == True:
                        ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
                    else:
                        pass
                    if show_nws_firewx_zones == True:
                        ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
                    else:
                        pass
                    if show_nws_public_zones == True:
                        ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
                    else:
                        pass
            
                    model = model.upper()
                    
                    if use_wind_gust == False:
                        plt.title(f"{model} FAVORABLE FIREWX CONDITIONS (SHADED RED)\n[T >= {temperature_threshold} [°F] & RH <= {low_rh_threshold} [%] & SUSTAINED WIND SPEED >= {high_wind_threshold} [MPH]]", fontsize=9, fontweight='bold', loc='left')
                        ax.text(x, y, f"KEY: T = ORANGE | RH = GREEN | SUSTAINED WIND = BARBS & CYAN", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
        
                    if use_wind_gust == True:
                        plt.title(f"{model} FAVORABLE FIREWX CONDITIONS (SHADED RED)\n[T >= {temperature_threshold} [°F] & RH <= {low_rh_threshold} [%] & WIND GUST >= {high_wind_threshold} [MPH]]", fontsize=9, fontweight='bold', loc='left')
                        ax.text(x, y, f"KEY: T = ORANGE | RH = GREEN | SUSTAINED WIND = BARBS | WIND GUSTS = CYAN", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props, zorder=11)
                        
                    plt.title("Forecast Valid: " +times.strftime('%a %d/%H UTC')+"\nInitialization: "+inits.strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
                    ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
                    ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
                    ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
                    
                    lon_2d, lat_2d = np.meshgrid(ds_list[i]['longitude'], ds_list[i]['latitude'])
        
                    numbers = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                                     transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
            
                    barbs = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate], lat_2d[::decimate, ::decimate],
                                     transform=ccrs.PlateCarree(), zorder=3, fontsize=8, clip_on=True)
    
                        
        
                    rh = rh[::decimate, ::decimate].to_numpy().flatten()
                    
                    temp = temp[::decimate, ::decimate].to_numpy().flatten()
    
                    wind_speed = wind_speed[::decimate, ::decimate].to_numpy().flatten()
    
                    barbs.plot_barb(u_wind[::decimate, ::decimate], v_wind[::decimate, ::decimate], color='black', alpha=1, zorder=3, linewidth=0.5)
            
                    numbers.plot_parameter('SW', rh, color='lime', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
                    numbers.plot_parameter('NW', temp, color='darkorange', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
                    numbers.plot_parameter('SE', wind_speed, color='cyan', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
        
                    try:
                        ax.pcolormesh(mask['longitude'], mask['latitude'], mask[:, :], transform=datacrs, cmap=cmap, zorder=1, alpha=0.5)
                    except Exception as e:
                        pass
            
                    fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                    plt.close(fig)
                    if mapcrs == datacrs:
                        tim.sleep(10)

        print(f"Saved forecast graphics to {path_print}.")

class precipitation:


    r'''
    This class hosts the functions showing the precipitation forecast.

    '''

    def plot_precipitation_rate(model, region, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States & Counties', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-', x1=0.01, y1=-0.03, x2=0.725, y2=-0.025, x3=0.01, y3=0.01, shrink=1, decimate=7, signature_fontsize=6, stamp_fontsize=5, sample_point_fontsize=8, x=0.01, y=0.97):

        r'''
        This function plots the Precipitation Rate Forecast. 

        Required Arguments: 
        
        1) model (String) - This is the model the user must select. 
                               
           Here are the choices: 
           1) GFS0p25 - GFS 0.25x0.25 degree
           2) GFS0p50 - GFS 0.5x0.5 degree
           3) GFS1p00 - GFS 1.0x1.0 degree
           4) GEFS0p50 - GEFS 0.5x0.5 degree
           5) CMCENS - Canadian Ensemble
           6) NAM - North American Model
           7) NA NAM - 32km North American Model - Full North America
           8) RAP - Rapid Refresh Model
           9) RAP 32 - 32km Rapid Refresh Model - Full North America
    
        2) region (String) - This is the region the user wishes to look at. There are a lot of preset regions. 
                             To look at any state use the 2-letter abbreviation for the state in either all capitals
                             or all lowercase. For CONUS, use CONUS in all caps or lower case. For a broad view of the
                             CONUS, Southern Canada and Northern Mexico use: 'CONUS & South Canada & North Mexico'. For 
                             North America use either: NA, na, North America or north america. If the user wishes to use custom
                             boundaries, then enter 'Custom' or 'custom'. For Geographic Area Coordination Centers you can use 
                             the 4-letter abbreviation in all caps or lower case so for example you would use either 'OSCC' or 
                             'oscc' for South Ops. 
    
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
    
        7) show_rivers (Boolean) - If set to True, rivers will display. If set to False, county borders will not display. 
            Default setting is True. Users should change this value to False if they wish to hide rivers.
    
        8) reference_system (String) - Default = 'States & Counties'. The georgraphical reference system with respect to the borders on the map. If the user
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
    
        31) x1 (Float) - Default = 0.01. The x-position of the signature text box with respect to the axis of the image. 
    
        32) y1 (Float) - Default = -0.03. The y-position of the signature text box with respect to the axis of the image. 
    
        33) x2 (Float) - Default = 0.725. The x-position of the timestamp text box with respect to the axis of the image.
    
        34) y2 (Float) - Default = -0.025. The y-position of the timestamp text box with respect to the axis of the image.
    
        35) x3 (Float) - Default = 0.01. The x-position of the reference system text box with respect to the axis of the image.
    
        36) y3 (Float) - Default = 0.01. The y-position of the reference system text box with respect to the axis of the image.
    
        37) shrink (Float) - Default = 1. This is how the colorbar is sized to the figure. 
                                          This is a feature of matplotlib, as per their definition, the shrink is:
                                          "Fraction by which to multiply the size of the colorbar." 
                                          This should only be changed if the user wishes to make a custom plot. 
                                          Preset values are called from the settings module for each region. 
    
        38) decimate (Integer) - Default = 7. This determines how far spaced apart the points are when plotting the values overlaying the shading. 
                                 Higher numbers result in more sparse numbers or modeled station plots or wind barbs etc. This is only to be changed
                                 when making a custom plot. 
    
        39) signature_fontsize (Integer) - Default = 6. The fontsize of the signature. This is only to be changed when making a custom plot. 
    
        40) stamp_fontsize (Integer) - Default = 5. The fontsize of the timestamp and reference system text. This is only to be changed when making a custom plot. 
    
        41) sample_point_fontsize (Integer) - Default = 8. The fontsize of the sample points on the image. This is only to be changed when making a custom plot.
    
        42) x (Float) - Default = 0.01. The x-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot.
    
        43) y (Float) - Default = 0.97. The y-position of the textbox with respect to the axis of the image showing the value of the contour line. This is only to be changed when making a custom plot. 
    
    
        Returns: Images for the various different forecast times saved to the path: f: Weather Data/Forecast Model Data/model/region/reference system/parameter(s)/level


        '''
    
        data=data
        ds=ds
        western_bound=western_bound
        eastern_bound=eastern_bound 
        southern_bound=southern_bound
        northern_bound=northern_bound
        show_rivers=show_rivers
        reference_system=reference_system
        state_border_linewidth=state_border_linewidth
        county_border_linewidth=county_border_linewidth
        gacc_border_linewidth=gacc_border_linewidth
        psa_border_linewidth=psa_border_linewidth 
        cwa_border_linewidth=cwa_border_linewidth
        nws_firewx_zones_linewidth=nws_firewx_zones_linewidth 
        nws_public_zones_linewidth=nws_public_zones_linewidth 
        state_border_linestyle=state_border_linestyle
        county_border_linestyle=county_border_linestyle
        gacc_border_linestyle=gacc_border_linestyle
        psa_border_linestyle=psa_border_linestyle 
        cwa_border_linestyle=cwa_border_linestyle
        nws_firewx_zones_linestyle=nws_firewx_zones_linestyle 
        nws_public_zones_linestyle=nws_public_zones_linestyle
        x1=x1 
        y1=y1
        x2=x2
        y2=y2 
        x3=x3
        y3=y3 
        shrink=shrink
        sample_point_fontsize=sample_point_fontsize
        x=x 
        y=y
        PSAs = geometry.get_shapes(f"PSA Shapefiles/National_PSA_Current.shp")
        
        GACC = geometry.get_shapes(f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        
        CWAs = geometry.get_shapes(f"NWS CWA Boundaries/w_05mr24.shp")
        
        FWZs = geometry.get_shapes(f"NWS Fire Weather Zones/fz05mr24.shp")
        
        PZs = geometry.get_shapes(f"NWS Public Zones/z_05mr24.shp")
    
        levels = [0.01, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.5, 2, 2.5, 3]
        ticks = levels
    
        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            mapcrs = ccrs.LambertConformal()
        else:
            mapcrs = ccrs.PlateCarree()
    
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
    
        str_level = f"SURFACE"
    
        if model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM' or model == 'RAP' or model == 'RAP 32':
            step = 1
        
        if model == 'CMCENS' or model == 'GEFS0p50':
            step = 1
            
        if model == 'GFS0p25' or model == 'GFS0p25_1h':
            step = 2
            
        if model == 'GFS0p50':
            step = 2
        
        if model == 'GFS1p00':
            step = 2
    
    
        if western_bound != None and eastern_bound != None and southern_bound != None and northern_bound != None:
            wb=western_bound
            eb=eastern_bound
            sb=southern_bound
            nb=northern_bound
            x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y = x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize, sample_point_fontsize, x, y
        else:
            wb, eb, sb, nb, x1, y1, x2, y2, x3, y3, shrink, decimate, signature_fontsize, stamp_fontsize = settings.get_region_info(model, region)
            sample_point_fontsize, x, y = settings.get_sp_dims_and_textbox_coords(region)

            if model == 'GFS0p25' or model == 'GFS0p25_1h' or model == 'GEFS0p25 ENS MEAN':
                
                if region == 'conus' or region == 'North America' or region == 'north america' or region == 'NA' or region == 'na':
                    decimate = decimate * 2
                else:
                    decimate = decimate + 1
                    
            elif model == 'NAM 1hr' or model == 'NAM' or model == 'NA NAM':
                if region == 'conus' or region == 'North America' or region == 'north america' or region == 'NA' or region == 'na':
                    decimate = decimate * 2
                else:
                    decimate = decimate + 2
            else:
                decimate = decimate

        path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, 'Precipitation Rate', str_level)
    
        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
                
        if data == False:
            if model == 'RAP' or model == 'RAP 32':
                ds = model_data.get_hourly_rap_data_area_forecast(model, region, wb, eb, sb, nb)
            else:
                ds = model_data.get_nomads_opendap_data(model, region, wb, eb, sb, nb)
            
        if data == True:
            ds = ds

    
        cmap = colormaps.precipitation_colormap()

    
        end1 = (int(round((len(ds['time']) - 1)/6, 0)) - 1)
        end2 = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()
        
        for t in range(0, end1, 1):
        
            fname = f"Image_{t}.png"
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            model = model.upper()
            plt.title(f"{model} SURFACE PRECIPITATION RATE [IN/HR]", fontsize=9, fontweight='bold', loc='left')
            plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
            
            lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
    
            stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                             transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
    
            if model == 'CMCENS' or model == 'GEFS0P50':
    
                qpf = ds['pratesfc'][0, t, :, :] * 141.73236
    
                qpf = qpf[::decimate, ::decimate].to_numpy().flatten()
        
                stn.plot_parameter('C', qpf, color='white', formatter='0.2f', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
                cs = ax.contourf(ds['lon'], ds['lat'], (ds['pratesfc'][0, t, :, :] * 141.73236), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='max')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
    
    
            else:
                
                qpf = ds['pratesfc'][t, :, :] * 141.73236
    
                qpf = qpf[::decimate, ::decimate].to_numpy().flatten()
        
                stn.plot_parameter('C', qpf, color='white', formatter='0.2f', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
                cs = ax.contourf(ds['lon'], ds['lat'], (ds['pratesfc'][t, :, :] * 141.73236), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='max')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
    
        for t in range(end1, end2, step):
        
            fname = f"Image_{t}.png"
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.BORDERS, linewidth=1, zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            ax.add_feature(provinces, linewidth=province_border_linewidth, zorder=1)
            if show_rivers == True:
                ax.add_feature(cfeature.RIVERS, color='lightcyan', zorder=4)
            else:
                pass
        
            if show_gacc_borders == True:
                ax.add_feature(GACC, linewidth=gacc_border_linewidth, linestyle=gacc_border_linestyle, zorder=6)
            else:
                pass
            if show_psa_borders == True:
                ax.add_feature(PSAs, linewidth=psa_border_linewidth, linestyle=psa_border_linestyle, zorder=5)
            else:
                pass
            if show_county_borders == True:
                ax.add_feature(USCOUNTIES, linewidth=county_border_linewidth, linestyle=county_border_linestyle, zorder=5)
            else:
                pass
            if show_state_borders == True:
                ax.add_feature(cfeature.STATES, linewidth=state_border_linewidth, linestyle=state_border_linestyle, edgecolor='black', zorder=6)
            else:
                pass
            if show_cwa_borders == True:
                ax.add_feature(CWAs, linewidth=cwa_border_linewidth, linestyle=cwa_border_linestyle, zorder=5)
            else:
                pass
            if show_nws_firewx_zones == True:
                ax.add_feature(FWZs, linewidth=nws_firewx_zones_linewidth, linestyle=nws_firewx_zones_linestyle, zorder=5)
            else:
                pass
            if show_nws_public_zones == True:
                ax.add_feature(PZs, linewidth=nws_public_zones_linewidth, linestyle=nws_public_zones_linestyle, zorder=5)
            else:
                pass
    
            model = model.upper()
            plt.title(f"{model} SURFACE PRECIPITATION RATE [IN/HR]", fontsize=9, fontweight='bold', loc='left')
            plt.title("Forecast Valid: " +times.iloc[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times.iloc[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            ax.text(x1, y1, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=signature_fontsize, fontweight='bold', bbox=props)
            ax.text(x2, y2, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props)
            ax.text(x3, y3, "Reference System: "+reference_system, transform=ax.transAxes, fontsize=stamp_fontsize, fontweight='bold', bbox=props, zorder=11)
            
            lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
    
            stn = mpplots.StationPlot(ax, lon_2d[::decimate, ::decimate].flatten(), lat_2d[::decimate, ::decimate].flatten(),
                             transform=ccrs.PlateCarree(), zorder=3, fontsize=sample_point_fontsize, clip_on=True)
    
            if model == 'CMCENS' or model == 'GEFS0P50':
    
                qpf = ds['pratesfc'][0, t, :, :] * 141.73236
    
                qpf = qpf[::decimate, ::decimate].to_numpy().flatten()
        
                stn.plot_parameter('C', qpf, color='white', formatter='0.2f', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
                cs = ax.contourf(ds['lon'], ds['lat'], (ds['pratesfc'][0, t, :, :] * 141.73236), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='max')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
    
    
            else:
                
                qpf = ds['pratesfc'][t, :, :] * 141.73236 
    
                qpf = qpf[::decimate, ::decimate].to_numpy().flatten()
        
                stn.plot_parameter('C', qpf, color='white', formatter='0.2f', path_effects=[withStroke(linewidth=1, foreground='black')], zorder=7)
    
                cs = ax.contourf(ds['lon'], ds['lat'], (ds['pratesfc'][t, :, :] * 141.73236), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='max')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
                plt.close(fig)
                if mapcrs == datacrs:
                    tim.sleep(10)
        print(f"Saved forecast graphics to {path_print}.")
