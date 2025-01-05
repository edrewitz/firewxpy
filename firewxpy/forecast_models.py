import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import metpy.plots as mpplots
import metpy.calc as mpcalc
import numpy as np
import parsers as parsers
import geometry as geometry
import colormaps as colormaps
import pandas as pd
import matplotlib.gridspec as gridspec
import settings as settings
import standard as standard
import dims as dims
import os

from matplotlib.patheffects import withStroke
from metpy.plots import USCOUNTIES
from datetime import datetime, timedelta
from dateutil import tz
from calc import scaling, Thermodynamics, unit_conversion
from utilities import file_functions
from metpy.units import units
from data_access import model_data

mpl.rcParams['font.weight'] = 'bold'
local_time, utc_time = standard.plot_creation_time()
mapcrs = ccrs.LambertConformal()
datacrs = ccrs.PlateCarree()

provinces = cfeature.NaturalEarthFeature(category='cultural', 
    name='admin_1_states_provinces_lines', scale='50m', facecolor='none', edgecolor='k')

props = dict(boxstyle='round', facecolor='wheat', alpha=1)

class dynamics:


    def plot_500mb_vorticity_height_wind(model, region, western_bound=None, eastern_bound=None, southern_bound=None, northern_bound=None, ds=None, show_counties=False):

        model = model
        region = region
        western_bound=western_bound
        eastern_bound=eastern_bound
        southern_bound=southern_bound
        northern_bound=northern_bound 

        if model == 'NAM':
            idx = 20
        else:
            idx = 12


        if region == 'CONUS & South Canada & North Mexico':
            wb, eb, sb, nb = -130, -60, 20, 60
            shrink=0.55
        if region == 'CONUS' or region =='conus':
            wb, eb, sb, nb = -125, -65, 23, 50
            shrink = 0.45
        if region == 'AK' or region == 'ak':
            wb, eb, sb, nb = -125, -65, 23, 50
            shrink = 0.7
        if region == 'NA' or region == 'na' or region == 'North America' or region == 'north america':
            wb, eb, sb, nb = -180, -45, 20, 85
            shrink=0.7
        
        if ds == None:
            ds = model_data.get_nomads_opendap_data(model, region, western_bound, eastern_bound, southern_bound, northern_bound, dynamic=True)
        else:
            ds = ds
        
        cmap = colormaps.vorticity_colormap()

        end = len(ds['time']) - 1
        time = ds['time']
        times = time.to_pandas()
        
        path, path_print = file_functions.forecast_model_graphics_paths(model, region, 'Z500_Vorticity_Wind')

        for file in os.listdir(f"{path}"):
            try:
                os.remove(f"{path}/{file}")
                print(f"Old Image Removed.")
            except Exception as e:
                pass
        
        for t in range(0, end, 2):
        
            fname = f"Image_{t}.png"
        
            fig = plt.figure(figsize=(12, 12))
            fig.set_facecolor('aliceblue')
            
            ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
            ax.set_extent([wb, eb, sb, nb], datacrs)
            ax.add_feature(cfeature.COASTLINE.with_scale('50m'), linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.STATES, linewidth=0.75, zorder=9)
            ax.add_feature(cfeature.LAND, color='beige', zorder=1)
            ax.add_feature(cfeature.OCEAN, color='lightcyan', zorder=1)
            ax.add_feature(cfeature.LAKES, color='lightcyan', zorder=1)
            if show_counties == True:
                ax.add_feature(USCOUNTIES, linewidth=0.25, zorder=1)
            ax.add_feature(provinces, linewidth=0.5, zorder=1)
            
            plt.title(f"{model} 500 MB GPH [Dm]/ABS VORT [1/s]/WIND [kts]", fontsize=9, fontweight='bold', loc='left')
            plt.title("Forecast Valid: " +times[t].strftime('%a %d/%H UTC')+"\nInitialization: "+times[0].strftime('%a %d/%H UTC'), fontsize=7, fontweight='bold', loc='right')
            ax.text(0.01, -0.03, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: NOAA/NCEP/NOMADS", transform=ax.transAxes, fontsize=6, fontweight='bold', bbox=props)
            ax.text(0.68, -0.025, "Image Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=5, fontweight='bold', bbox=props)
            
            lon_2d, lat_2d = np.meshgrid(ds['lon'], ds['lat'])
            
            stn = mpplots.StationPlot(ax, lon_2d[::10, ::10], lat_2d[::10, ::10],
                             transform=ccrs.PlateCarree(), zorder=3, fontsize=5, clip_on=True)
            
            stn.plot_barb((ds['ugrdprs'][t, idx, ::10, ::10] * 1.94384), (ds['vgrdprs'][t, idx, ::10, ::10] * 1.94384), color='black', alpha=1, zorder=3, linewidth=0.25)
            
            c_neg = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, idx, :, :]/10), levels=np.arange(440, 540, 4), colors='darkblue', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
            c = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, idx, :, :]/10), levels=[540], colors='black', zorder=2, transform=datacrs, linewidths=1)
            c_pos = ax.contour(ds['lon'], ds['lat'], (ds['hgtprs'][t, idx, :, :]/10), levels=np.arange(544, 624, 4), colors='darkred', zorder=2, transform=datacrs, linewidths=0.5, linestyles='--')
            ax.clabel(c_neg, levels=np.arange(440, 540, 4), inline=True, fontsize=8, rightside_up=True)
            ax.clabel(c, levels=[540], inline=True, fontsize=8, rightside_up=True)
            ax.clabel(c_pos, levels=np.arange(544, 624, 4), inline=True, fontsize=8, rightside_up=True)
            
            cs = ax.contourf(ds['lon'], ds['lat'], ds['absvprs'][t, idx, :, :], cmap=cmap, transform=datacrs, levels=np.arange(0, 55e-5, 50e-6), alpha=0.35, extend='max')
            cbar = fig.colorbar(cs, shrink=shrink, pad=0.01, location='right', format="{x:.0e}")
        
            fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        
            print(f"Saved image for forecast {times[t].strftime('%a %d/%H UTC')} to {path_print}.")


























