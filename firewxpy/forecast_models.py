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

mpl.rcParams['font.weight'] = 'bold'
local_time, utc_time = standard.plot_creation_time()
mapcrs = ccrs.PlateCarree()
datacrs = ccrs.PlateCarree()

provinces = cfeature.NaturalEarthFeature(category='cultural', 
    name='admin_1_states_provinces_lines', scale='50m', facecolor='none', edgecolor='k')

props = dict(boxstyle='round', facecolor='wheat', alpha=1)

class dynamics:


    def plot_vorticity_geopotential_height_wind(model, region, level=500, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-'):
    
    
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
        
    
        if model == 'NAM 1hr':
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
    
        if region == 'CONUS & South Canada & North Mexico':
            wb, eb, sb, nb = -140, -45, 20, 65
            shrink = 0.4
            x1, y1 = 0.01, -0.03
            x2, y2 = 0.725, -0.025
            x3, y3 = 0.01, 0.01
        if region == 'CONUS' or region =='conus':
            wb, eb, sb, nb = -125, -65, 23, 50
            shrink = 0.4
            x1, y1 = 0.01, -0.03
            x2, y2 = 0.725, -0.025
            x3, y3 = 0.01, 0.01
        if region == 'AK' or region == 'ak':
            wb, eb, sb, nb = -180, -115, 45, 85
            shrink = 0.5
            x1, y1 = 0.01, -0.03
            x2, y2 = 0.725, -0.025
            x3, y3 = 0.01, 0.01
        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            wb, eb, sb, nb = -180, -45, 20, 85
            shrink=0.4
            x1, y1 = 0.01, -0.03
            x2, y2 = 0.68, -0.025
            x3, y3 = 0.01, 0.01
        
        if data == False:
            ds = model_data.get_nomads_opendap_data(model, region, western_bound, eastern_bound, southern_bound, northern_bound, dynamic=True)
            
        if data == True:
            ds = ds
    
    
        if model == 'CMCENS' or model == 'GEFS0p50':
            ds['absvprs'] = mpcalc.vorticity((ds['ugrdprs'][0, :, level_idx, :, :] * units('m/s')), (ds['vgrdprs'][0, :, level_idx, :, :] * units('m/s')))
    
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
                
        print(f"Any old images (if any) in {path_print} have been deleted.")
        
        for t in range(0, end, step):
        
            fname = f"Image_{t}.png"
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
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
            plt.title(f"{model} {str_level} GPH [Dm]/ABS VORT [1/s]/WIND [kts]", fontsize=9, fontweight='bold', loc='left')
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
                    
                cs = ax.contourf(ds['lon'], ds['lat'], ds['absvprs'][t, :, :], cmap=cmap, transform=datacrs, levels=np.arange(0, 55e-5, 50e-6), alpha=0.35, extend='max')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', format="{x:.0e}")
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        
                print(f"Saved image for forecast {times.iloc[t].strftime('%a %d/%H UTC')} to {path_print}.")
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
                
                cs = ax.contourf(ds['lon'], ds['lat'], ds['absvprs'][t, level_idx, :, :], cmap=cmap, transform=datacrs, levels=np.arange(0, 55e-5, 50e-6), alpha=0.35, extend='max')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', format="{x:.0e}")
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            
                print(f"Saved image for forecast {times.iloc[t].strftime('%a %d/%H UTC')} to {path_print}.")
                tim.sleep(10)
    
    
    def plot_geopotential_height(model, region, level=500, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-'):
    
    
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
        
    
        if model == 'NAM 1hr':
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
    
        if region == 'CONUS & South Canada & North Mexico':
            wb, eb, sb, nb = -140, -45, 20, 65
            shrink = 0.4
            x1, y1 = 0.01, -0.03
            x2, y2 = 0.725, -0.025
            x3, y3 = 0.01, 0.01
        if region == 'CONUS' or region =='conus':
            wb, eb, sb, nb = -125, -65, 23, 50
            shrink = 0.4
            x1, y1 = 0.01, -0.03
            x2, y2 = 0.725, -0.025
            x3, y3 = 0.01, 0.01
        if region == 'AK' or region == 'ak':
            wb, eb, sb, nb = -180, -115, 45, 85
            shrink = 0.5
            x1, y1 = 0.01, -0.03
            x2, y2 = 0.725, -0.025
            x3, y3 = 0.01, 0.01
        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            wb, eb, sb, nb = -180, -45, 20, 85
            shrink=0.4
            x1, y1 = 0.01, -0.03
            x2, y2 = 0.68, -0.025
            x3, y3 = 0.01, 0.01
        
        if data == False:
            ds = model_data.get_nomads_opendap_data(model, region, western_bound, eastern_bound, southern_bound, northern_bound, dynamic=True)
            
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
                
        print(f"Any old images (if any) in {path_print} have been deleted.")
        
        for t in range(0, end, step):
        
            fname = f"Image_{t}.png"
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
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
            plt.title(f"{model} {str_level} GEOPOTENTIAL HEIGHT [Dm]", fontsize=9, fontweight='bold', loc='left')
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
        
                print(f"Saved image for forecast {times.iloc[t].strftime('%a %d/%H UTC')} to {path_print}.")
                tim.sleep(10)
    
    
            else:
                
                c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), levels=levels, colors='black', zorder=2, transform=datacrs, linewidths=1)
                ax.clabel(c, levels=levels, inline=True, fontsize=8, rightside_up=True)
                
                cs = ax.contourf(ds['lon'], ds['lat'], (ds['hgtprs'][t, level_idx, :, :]/10), cmap=cmap, transform=datacrs, levels=levels, alpha=0.35, extend='both')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=ticks)
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            
                print(f"Saved image for forecast {times.iloc[t].strftime('%a %d/%H UTC')} to {path_print}.")
                tim.sleep(10)


    def plot_24hr_geopotential_height_change(model, region, level=500, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-'):
    
    
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
    
        if region == 'CONUS & South Canada & North Mexico':
            wb, eb, sb, nb = -140, -45, 20, 65
            shrink = 0.4
            x1, y1 = 0.01, -0.03
            x2, y2 = 0.725, -0.025
            x3, y3 = 0.01, 0.01
        if region == 'CONUS' or region =='conus':
            wb, eb, sb, nb = -125, -65, 23, 50
            shrink = 0.4
            x1, y1 = 0.01, -0.03
            x2, y2 = 0.725, -0.025
            x3, y3 = 0.01, 0.01
        if region == 'AK' or region == 'ak':
            wb, eb, sb, nb = -180, -115, 45, 85
            shrink = 0.5
            x1, y1 = 0.01, -0.03
            x2, y2 = 0.725, -0.025
            x3, y3 = 0.01, 0.01
        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            wb, eb, sb, nb = -180, -45, 20, 85
            shrink=0.4
            x1, y1 = 0.01, -0.03
            x2, y2 = 0.68, -0.025
            x3, y3 = 0.01, 0.01
        
        if data == False:
            ds = model_data.get_nomads_opendap_data(model, region, western_bound, eastern_bound, southern_bound, northern_bound, dynamic=True)
            
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
                
        print(f"Any old images (if any) in {path_print} have been deleted.")
        
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
            plt.title(f"{model} {str_level} 24-HR GEOPOTENTIAL HEIGHT CHANGE [ΔDm]", fontsize=9, fontweight='bold', loc='left')
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
            
                    print(f"Saved image for forecast {times.iloc[t1].strftime('%a %d/%H UTC')} to {path_print}.")
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
                
                    print(f"Saved image for forecast {times.iloc[t1].strftime('%a %d/%H UTC')} to {path_print}.")
                    tim.sleep(10)
                except Exception as e:
                    pass


    def plot_geopotential_height_wind(model, region, level=250, data=False, ds=None, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, show_rivers=False, reference_system='States Only', show_state_borders=False, show_county_borders=False, show_gacc_borders=False, show_psa_borders=False, show_cwa_borders=False, show_nws_firewx_zones=False, show_nws_public_zones=False, state_border_linewidth=1, province_border_linewidth=1, county_border_linewidth=0.25, gacc_border_linewidth=1, psa_border_linewidth=0.25, cwa_border_linewidth=1, nws_firewx_zones_linewidth=0.25, nws_public_zones_linewidth=0.25,  state_border_linestyle='-', county_border_linestyle='-', gacc_border_linestyle='-', psa_border_linestyle='-', cwa_border_linestyle='-', nws_firewx_zones_linestyle='-', nws_public_zones_linestyle='-'):
    
    
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
            speeds = np.arange(20, 91, 1)
            speed_ticks = speeds[::5]
        if level == 700:
            levels = np.arange(240, 340, 4)
            speeds = np.arange(20, 91, 1)
            speed_ticks = speeds[::5]
        if level == 500:
            speeds = np.arange(50, 126, 1)
            speed_ticks = speeds[::5]
        if level == 300:
            levels = np.arange(840, 1020, 10)
            speeds = np.arange(75, 151, 1)
            speed_ticks = speeds[::5]
        if level == 250:
            levels = np.arange(900, 1140, 10)
            speeds = np.arange(75, 151, 1)
            speed_ticks = speeds[::5]
        if level == 200:
            levels = np.arange(1000, 1280, 10)   
            speeds = np.arange(75, 151, 1)
            speed_ticks = speeds[::5]
    
        if model == 'NAM 1hr':
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
    
        if region == 'CONUS & South Canada & North Mexico':
            wb, eb, sb, nb = -140, -45, 20, 65
            shrink = 0.4
            x1, y1 = 0.01, -0.03
            x2, y2 = 0.725, -0.025
            x3, y3 = 0.01, 0.01
        if region == 'CONUS' or region =='conus':
            wb, eb, sb, nb = -125, -65, 23, 50
            shrink = 0.4
            x1, y1 = 0.01, -0.03
            x2, y2 = 0.725, -0.025
            x3, y3 = 0.01, 0.01
        if region == 'AK' or region == 'ak':
            wb, eb, sb, nb = -180, -115, 45, 85
            shrink = 0.5
            x1, y1 = 0.01, -0.03
            x2, y2 = 0.725, -0.025
            x3, y3 = 0.01, 0.01
        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            wb, eb, sb, nb = -180, -45, 20, 85
            shrink=0.4
            x1, y1 = 0.01, -0.03
            x2, y2 = 0.68, -0.025
            x3, y3 = 0.01, 0.01
        
        if data == False:
            ds = model_data.get_nomads_opendap_data(model, region, western_bound, eastern_bound, southern_bound, northern_bound, dynamic=True)
            
        if data == True:
            ds = ds
    
        cmap = colormaps.jet_stream_colormap()
    
        end = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()
    
    
        path, path_print = file_functions.forecast_model_graphics_paths(model, region, reference_system, 'Geopotential Height & Wind', str_level)
    
        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
            except Exception as e:
                pass
                
        print(f"Any old images (if any) in {path_print} have been deleted.")
        
        for t in range(0, end, step):
        
            fname = f"Image_{t}.png"
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
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
            plt.title(f"{model} {str_level} GPH [Dm]/WIND [kts]", fontsize=9, fontweight='bold', loc='left')
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
                    
                cs = ax.contourf(ds['lon'], ds['lat'], (mpcalc.wind_speed((ds['ugrdprs'][0, t, level_idx, :, :] *units('m/s')), (ds['vgrdprs'][0, t, level_idx, :, :] *units('m/s'))) * 1.94384), cmap=cmap, transform=datacrs, levels=speeds, alpha=0.35, extend='max')
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=speed_ticks)
    
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        
                print(f"Saved image for forecast {times.iloc[t].strftime('%a %d/%H UTC')} to {path_print}.")
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
                cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', ticks=speed_ticks)
        
                fig.savefig(f"{path}/{fname}", bbox_inches='tight')
            
                print(f"Saved image for forecast {times.iloc[t].strftime('%a %d/%H UTC')} to {path_print}.")
                tim.sleep(10)









