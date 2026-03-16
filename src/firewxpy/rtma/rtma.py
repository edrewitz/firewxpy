"""
This file hosts the functions for the CONUS Real Time Mesoscale Analysis (RTMA) Graphics

(C) Eric J. Drewitz 2024 - 2026
"""
import warnings as _warnings
_warnings.filterwarnings('ignore')
import matplotlib as _mpl 

import matplotlib.pyplot as _plt 
import matplotlib.colors as _mcolors
import cartopy.crs as _ccrs 
import cartopy.feature as _cfeature 
import metpy.plots as _mpplots
import numpy as _np
import pandas as _pd

from dateutil import tz as _tz
from matplotlib.patheffects import withStroke as _withStroke
from firewxpy.utils.station_plot_formatting import fix_var_array as _fix_var_array
from firewxpy.utils.directory import build_directory_branch as _build_directory_branch
from firewxpy.utils.plot_coords import bounding_box as _bounding_box
from firewxpy.utils.standard import(
    get_timezone_abbreviation as _get_timezone_abbreviation,
    plot_creation_time as _plot_creation_time
)
from firewxpy.utils.geometry import(
    import_shapefile_from_web as _import_shapefile_from_web,
    import_shapefile_local as _import_shapefile_local,
    import_geojson_from_web as _import_geojson_from_web,
    import_geojson_local as _import_geojson_local,
    get_filename_from_url as _get_filename_from_url
)
from wxdata import(
    rtma as _rtma,
    rtma_comparison as _rtma_comparison
)

_local, _utc = _plot_creation_time()
_timezone = _get_timezone_abbreviation()
_from_zone = _tz.tzutc()
_to_zone = _tz.tzlocal()
_mpl.rcParams['font.weight'] = 'bold'

def plot_temperature(region='conus',
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
                     decimate=50,
                     start=-30,
                     stop=130,
                     step=1,
                     facecolor='aliceblue',
                     primary_title_text='RTMA',
                     primary_title_textbox_color='wheat',
                     primary_title_textbox_style='round',
                     primary_title_textbox_alpha=1,
                     secondary_title_textbox_color='wheat',
                     secondary_title_textbox_style='round',
                     secondary_title_textbox_alpha=1,
                     primary_title_fontsize=12,
                     secondary_title_fontsize=10,
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
                     colorbar_interval=10,
                     colorbar_aspect=50,
                     colormap='jet',
                     contourf_alpha=0.5,
                     contourf_zorder=2,
                     colors=['magenta',
                             'orchid',
                             'plum',
                             'darkviolet',
                             'darkslateblue',
                             'blue',
                             'cyan',
                             'lawngreen',
                             'greenyellow',
                             'olive',
                             'gold',
                             'goldenrod',
                             'darkorange',
                             'deeppink',
                             'crimson',
                             'darkred',
                             'grey'],
                     ds=None,
                     western_bound=-125,
                     eastern_bound=-65,
                     southern_bound=20,
                     northern_bound=50,
                     pixel_query_value_fontsize=4,
                     pixel_query_value_zorder=7,
                     pixel_query_value_foreground='white',
                     pixel_query_value_fontcolor='black',
                     path='FireWxPy Graphics/RTMA/Temperature',
                     filename='RTMA Temperature.png',
                     proxies=None,
                     clear_recycle_bin=False,
                     clear_data=True,
                     chunk_size=8192,
                     notifications='off',
                     convert_temperature=True,
                     convert_to='fahrenheit',
                     custom_data_directory=None,
                     temperature_var_key='2m_temperature',
                     longitude_key='longitude',
                     latitude_key='latitude'):
    
    
    _build_directory_branch(f"{path}/{region.upper()}/{reference_system.upper()}")
    
    _mpl.rcParams['xtick.labelsize'] = tick_label_fontsize
    _mpl.rcParams['ytick.labelsize'] = tick_label_fontsize
    
    primary_title_box = dict(boxstyle=primary_title_textbox_style, 
                            facecolor=primary_title_textbox_color, 
                            alpha=primary_title_textbox_alpha)
    
    secondary_title_box = dict(boxstyle=secondary_title_textbox_style, 
                            facecolor=secondary_title_textbox_color, 
                            alpha=secondary_title_textbox_alpha)
    
    signature_box = dict(boxstyle=signature_textbox_style, 
                            facecolor=signature_textbox_color, 
                            alpha=signature_textbox_alpha)
    
    reference_system_box = dict(boxstyle=reference_system_textbox_style, 
                            facecolor=reference_system_textbox_color, 
                            alpha=reference_system_textbox_alpha)
    
    levels = _np.arange(start, (stop + step), step)
    ticks = levels[::colorbar_interval]
    
    western_bound, eastern_bound, southern_bound, northern_bound = _bounding_box(region,
                                                                                 western_bound,
                                                                                 eastern_bound,
                                                                                 southern_bound,
                                                                                 northern_bound)
    
    if ds is None:
        ds = _rtma(proxies=proxies,
                   clear_recycle_bin=clear_recycle_bin,
                   clear_data=clear_data,
                   western_bound=western_bound,
                   eastern_bound=eastern_bound,
                   southern_bound=southern_bound,
                   northern_bound=northern_bound,
                   convert_temperature=convert_temperature,
                   convert_to=convert_to,
                   chunk_size=chunk_size,
                   notifications=notifications,
                   custom_directory=custom_data_directory)
    else:
        ds = ds
        
    if colormap == 'custom':
        cmap = _mcolors.LinearSegmentedColormap.from_list("temperature", colors)
    else:
        cmap = colormap
                
    vals = _fix_var_array(ds,
                        temperature_var_key,
                        0,
                        decimate)
    
    valid_time = _pd.to_datetime(ds['time'].to_pandas())
    valid_time = valid_time.tz_localize('UTC')
    time = valid_time.astimezone(_to_zone)
    time_utc = time.astimezone(_from_zone)
    
    fig = _plt.figure(figsize=(figure_x_length, figure_y_length))
    fig.set_facecolor(facecolor)
    
    ax = fig.add_subplot(1,1,1, projection=_ccrs.PlateCarree())
    ax.set_extent([western_bound, eastern_bound, southern_bound, northern_bound], _ccrs.PlateCarree())
    ax.add_feature(_cfeature.COASTLINE.with_scale('50m'), linewidth=coastline_linewidth, zorder=costline_zorder)
    ax.add_feature(_cfeature.LAND, color=land_color, zorder=land_zorder)
    ax.add_feature(_cfeature.OCEAN, color=ocean_color, zorder=ocean_zorder)
    ax.add_feature(_cfeature.LAKES, color=lakes_color, zorder=lakes_zorder)
    if show_rivers is True:
        ax.add_feature(_cfeature.RIVERS, color=rivers_color, zorder=rivers_zorder)
    if show_states is True:
        states = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_States_Territories.zip",
                                            f"Cartographic Files/US States",
                                            f"US_States_Territories.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            state_border_color)
        
        ax.add_geometries(states, 
                          crs=_ccrs.PlateCarree(), 
                          facecolor='none', 
                          edgecolor=state_border_color, 
                          linewidth=state_border_linewidth, 
                          zorder=state_border_zorder)
    
    if show_counties is True:
        counties = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/Geographic%20Boundaries/US_Counties.zip",
                                            f"Cartographic Files/US Counties",
                                            f"US_Counties.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            county_border_color)
        
        ax.add_geometries(counties, 
                          crs=_ccrs.PlateCarree(), 
                          facecolor='none', 
                          edgecolor=county_border_color, 
                          linewidth=county_border_linewidth, 
                          zorder=county_border_zorder)
        
    if show_gacc_boundaries is True:
        gacc = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/GACC_Boundaries_2026.zip",
                                            f"Cartographic Files/GACC Boundaries",
                                            f"GACC_Boundaries_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            gacc_border_color)
        
        ax.add_geometries(gacc, 
                          crs=_ccrs.PlateCarree(), 
                          facecolor='none', 
                          edgecolor=gacc_border_color, 
                          linewidth=gacc_border_linewidth, 
                          zorder=gacc_border_zorder)
    
    if show_predictive_services_areas is True:
        psa = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/USDA/USFS/PSA_Boundaries.zip",
                                            f"Cartographic Files/PSA Boundaries",
                                            f"PSA_Boundaries.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            predictive_services_areas_color)
        
        ax.add_geometries(psa, 
                          crs=_ccrs.PlateCarree(), 
                          facecolor='none', 
                          edgecolor=predictive_services_areas_color, 
                          linewidth=predictive_services_areas_linewidth, 
                          zorder=predictive_services_areas_zorder)
        
    if show_nws_public_zones is True:
        pz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Public_Zones_2026.zip",
                                            f"Cartographic Files/NWS Public Zones",
                                            f"NWS_Public_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_public_zones_color)
        
        ax.add_geometries(pz, 
                          crs=_ccrs.PlateCarree(), 
                          facecolor='none', 
                          edgecolor=nws_public_zones_color, 
                          linewidth=nws_public_zones_linewidth, 
                          zorder=nws_public_zones_zorder)
        
    if show_nws_fire_weather_zones is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_Fire_Weather_Zones_2026.zip",
                                            f"Cartographic Files/NWS Fire Weather Zones",
                                            f"NWS_Fire_Weather_Zones_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_fire_weather_zones_color)
        
        ax.add_geometries(fwz, 
                          crs=_ccrs.PlateCarree(), 
                          facecolor='none', 
                          edgecolor=nws_fire_weather_zones_color, 
                          linewidth=nws_fire_weather_zones_linewidth, 
                          zorder=nws_fire_weather_zones_zorder)
        
    if show_nws_cwa is True:
        fwz = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/NOAA/NWS_CWA_2026.zip",
                                            f"Cartographic Files/NWS CWAs",
                                            f"NWS_CWA_2026.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            nws_cwa_color)
        
        ax.add_geometries(fwz, 
                          crs=_ccrs.PlateCarree(), 
                          facecolor='none', 
                          edgecolor=nws_cwa_color, 
                          linewidth=nws_cwa_linewidth, 
                          zorder=nws_cwa_zorder)
        
    if show_calfire_boundaries is True:
        calfire = _import_shapefile_from_web(f"https://raw.githubusercontent.com/edrewitz/shapeography/refs/heads/main/CALFIRE/CalFire_Administrative_Units.zip",
                                            f"Cartographic Files/CalFire",
                                            f"CalFire_Administrative_Units.zip",
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            '.zip',
                                            calfire_boundary_color,
                                            convert_crs=True)
        
        ax.add_geometries(calfire, 
                          crs=_ccrs.PlateCarree(), 
                          facecolor='none', 
                          edgecolor=calfire_boundary_color, 
                          linewidth=calfire_boundary_linewidth, 
                          zorder=calfire_boundary_zorder)
        
    if custom_shapefile_url is not None:
        
        fname = _get_filename_from_url(custom_shapefile_url)
        
        custom_shape = _import_shapefile_from_web(custom_shapefile_url,
                                            f"Cartographic Files/{custom_shapefile_folder_name}",
                                            fname,
                                            proxies,
                                            chunk_size,
                                            notifications,
                                            refresh_cartographic_files,
                                            custom_shapefile_file_extension,
                                            custom_shapefile_color,
                                            convert_crs=convert_custom_shapefile_crs)
        
        ax.add_geometries(custom_shape, 
                          crs=_ccrs.PlateCarree(), 
                          facecolor='none', 
                          edgecolor=custom_shapefile_color, 
                          linewidth=custom_shapefile_linewidth, 
                          zorder=custom_shapefile_zorder)
        
    if custom_geojson_url is not None:
        
        custom_json = _import_geojson_from_web(custom_geojson_url,
                                                f"Cartographic Files/{custom_geojson_folder_name}", 
                                                custom_geojson_filename, 
                                                proxies, 
                                                chunk_size,
                                                notifications, 
                                                refresh_cartographic_files)
        
        ax.add_geometries(custom_json, 
                          crs=_ccrs.PlateCarree(), 
                          facecolor='none', 
                          edgecolor=custom_geojson_color, 
                          linewidth=custom_geojson_linewidth, 
                          zorder=custom_geojson_zorder)
        
    if custom_shapefile_local_path is not None:
        custom_local_shapefile = _import_shapefile_local(custom_shapefile_local_path,
                                                            custom_shapefile_local_color,
                                                            convert_crs=convert_local_custom_shapefile_crs)
        
        ax.add_geometries(custom_local_shapefile, 
                          crs=_ccrs.PlateCarree(), 
                          facecolor='none', 
                          edgecolor=custom_shapefile_local_color, 
                          linewidth=custom_shapefile_local_linewidth, 
                          zorder=custom_shapefile_local_zorder)
        
    if custom_geojson_local_path is not None:
        custom_local_geojson = _import_geojson_local(custom_geojson_local_path)
        
        ax.add_geometries(custom_local_geojson, 
                          crs=_ccrs.PlateCarree(), 
                          facecolor='none', 
                          edgecolor=custom_geojson_local_color, 
                          linewidth=custom_geojson_local_linewidth, 
                          zorder=custom_geojson_local_zorder)
    
    cs = ax.contourf(ds[longitude_key],
                ds[latitude_key],
                ds[temperature_var_key],
                cmap=cmap,
                levels=levels,
                transform=_ccrs.PlateCarree(),
                alpha=contourf_alpha,
                zorder=contourf_zorder,
                extend='both')
    
    fig.colorbar(cs, 
                shrink=colorbar_shrink, 
                pad=colorbar_pad, 
                location=colorbar_location,
                ticks=ticks,
                aspect=colorbar_aspect)
    
    _plt.title(f"{primary_title_text}", 
               fontsize=primary_title_fontsize, 
               fontweight='bold',
               bbox=primary_title_box,
               loc='left')
    
    if local_time is True:
        _plt.title(f"Valid: {time.strftime('%m/%d/%Y %H:00')} {_timezone}", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
    else:
        _plt.title(f"Valid: {time_utc.strftime('%m/%d/%Y %H:00')} UTC", 
                fontsize=secondary_title_fontsize, 
                fontweight='bold',
                bbox=secondary_title_box,
                loc='right')
        
    if signature_text_new_lines is False:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')} | Data Source: NCEP/NOMADS | Created: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    else:
        ax.text(signature_textbox_x_position, 
                signature_textbox_y_position,
                f"Plot Created With FireWxPy (C) Eric J. Drewitz 2024 - {_utc.strftime('%Y')}\nData Source: NCEP/NOMADS\nCreated: {_local.strftime('%m/%d/%Y %H:%M')} {_timezone} - {_utc.strftime('%m/%d/%Y %H:%M')} UTC",
                fontsize=signature_fontsize,
                fontweight='bold',
                bbox=signature_box,
                transform=ax.transAxes,
                zorder=signature_textbox_zorder)
    
    ax.text(reference_system_textbox_x_position, 
            reference_system_textbox_y_position,
            f"Reference System: {reference_system}",
            fontsize=reference_system_fontsize,
            fontweight='bold',
            bbox=reference_system_box,
            transform=ax.transAxes,
            zorder=reference_system_textbox_zorder)
        
    
    stn = _mpplots.StationPlot(ax, vals['longitude'], vals['latitude'],
                                 transform=_ccrs.PlateCarree(), fontsize=pixel_query_value_fontsize, zorder=pixel_query_value_zorder, clip_on=True)


    stn.plot_parameter('C', vals[temperature_var_key], color=pixel_query_value_fontcolor, path_effects=[_withStroke(linewidth=1, foreground=pixel_query_value_foreground)], zorder=pixel_query_value_zorder)
    
    fig.savefig(f"{path}/{region.upper()}/{reference_system.upper()}/{filename}", bbox_inches='tight')
    _plt.close(fig)
    if notifications == 'on':
        print(f"{filename} saved to {path}/{region.upper()}")