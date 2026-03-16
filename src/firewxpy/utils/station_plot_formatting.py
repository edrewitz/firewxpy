"""
This file hosts the function that returns a decimate dataframe for annotating station plots over a map of GRIB data.

(C) Eric J. Drewitz 2024-2026
"""

import warnings
warnings.filterwarnings('ignore')

def fix_var_array(ds,
                  parameter,
                  step,
                  decimate):
    
    try:
        stop = len(ds['step']) + step
    
        vals = []
        for i in range(0, stop, step):
            val = ds[parameter][i, ::decimate, ::decimate].to_dataframe()
            vals.append(val) 
        
    except Exception as e:
        vals = ds[parameter][::decimate, ::decimate].to_dataframe()
        
    return vals