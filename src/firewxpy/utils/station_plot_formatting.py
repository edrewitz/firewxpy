"""
This file hosts the function that returns a decimate dataframe for annotating station plots over a map of GRIB data.

(C) Eric J. Drewitz 2024-2026
"""

import warnings
import numpy as np
warnings.filterwarnings('ignore')

def fix_var_array(ds,
                  parameter,
                  step,
                  decimate):
    
    """
    This function fixes the GRIB data for overlaying onto a station plot.
    
    Required Arguments:
    
    1) ds (xarray.array) - The GRIB dataset.
    
    2) parameter (String) - Parameter key name.
    
    3) step (Integer) - The amount of steps.
    
    4) decimate (Integer) - This determines how the pixel queries appear on the map. Higher numbers
        equal more sparse and lower numbers equal less sparse. Use larger numbers for larger areas and smaller values for smaller areas. 
        
    Returns
    -------
    
    A list of Pandas.DataFrames to be used for plotting the station plots.
    """
    
    try:
        stop = len(ds['step']) + step
    
        vals = []
        for i in range(0, stop, step):
            val = ds[parameter][i, ::decimate, ::decimate].to_dataframe()
            vals.append(val) 
        
    except Exception as e:
        vals = ds[parameter][::decimate, ::decimate].to_dataframe()
        
    return vals

def fix_var_array_ndfd_hawaii(ds,
                  parameter,
                  decimate):
    
    """
    This function fixes the GRIB data for overlaying onto a station plot for NWS NDFD Hawaii Grids.
    
    Required Arguments:
    
    1) ds (xarray.array) - The GRIB dataset.
    
    2) parameter (String) - Parameter key name.
        
    3) decimate (Integer) - This determines how the pixel queries appear on the map. Higher numbers
        equal more sparse and lower numbers equal less sparse. Use larger numbers for larger areas and smaller values for smaller areas. 
        
    Returns
    -------
    
    An xarray.array used for plotting station plot overlays. 
    """
    

    lats = ds['latitude'].values
    lons = ds['longitude'].values
    ds[parameter] = ds

    lats_dec = lats[::decimate]
    lons_dec = lons[::decimate]
    lon2d_dec, lat2d_dec = np.meshgrid(lons_dec, lats_dec)
    vals_dec = ds[parameter][:, ::decimate, ::decimate].values
    stn_lons = lon2d_dec.ravel()
    stn_lats = lat2d_dec.ravel()
    stn_vals = vals_dec.ravel()

    return stn_lons, stn_lats, stn_vals