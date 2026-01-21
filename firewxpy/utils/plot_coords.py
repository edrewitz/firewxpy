"""
This file hosts the functions that affect the coordinates of the plots. 

(C) Eric J. Drewitz 2024-2026
"""

def bounding_box(region, 
                 western_bound,
                 eastern_bound,
                 southern_bound,
                 northern_bound):
    
    """
    This function returns the bounding box in lat/lon for each region.
    
    Required Arguments:
    
    1) region (String) - The name of the region.
    
    2) western_bound (Float or Integer) - The western bound in decimal degrees (-180 to 180).
    
    3) eastern_bound (Float or Integer) - The eastern bound in decimal degrees (-180 to 180).
    
    4) southern_bound (Float or Integer) - The southern bound in decimal degrees (-90 to 90).
    
    4) northern_bound (Float or Integer) - The northern bound in decimal degrees (-90 to 90).
    
    Optional Arguments: None
    
    Returns
    -------
    
    The bounding box coordinates for each region.    
    """
    
    region = region.lower()
    
    if region != 'custom':
    
        bounds = {
            
            'global':[-180, 180, -90, 90],
            'northern hemisphere':[-180, 180, 0, 90],
            'southern hemisphere':[-180, 180, -90, 0],
            'conus':[-126, -66, 24, 50.5],
            'ca':[-124.61, -113.93, 32.4, 42.5],
            'ak':[-170, -130, 50, 75],
            'hi':[-160.3, -154.73, 18.76, 22.28],
            'me':[-71.2, -66.75, 42.2, 47.6],
            'nh':[-72.65, -70.60, 42.35, 45.36],
            'vt':[-73.50, -71.44, 42.5, 45.10],
            'ma':[-73.55, -69.88, 41.3, 42.92],
            'ri':[-71.86, -71.11, 41.2, 42.03],
            'ct':[-73.74, -71.77, 40.8, 42.06],
            'nj':[-75.60, -73.5, 38.45, 41.37],
            'de':[-76, -74.5, 38.2, 39.9],
            'ny':[-79.85, -71.85, 40.3, 45.08],
            'pa':[-80.6, -74.6, 39.25, 42.32],
            'oh':[-84.9, -80.4, 37.75, 42],
            'mi':[-90.5, -82.31, 40.6, 48.26],
            'mn':[-97.45, -89.28, 42.85, 49.45],
            'wi':[-93.1, -86.68, 41.8, 47.11],
            'ia':[-96.77, -90, 39.9, 43.7],
            'in':[-88.19, -84.69, 37.1, 41.79],
            'mo':[-95.9, -88.92, 35.8, 40.66],
            'il':[-91.67, -87.44, 36.3, 42.55],
            'nd':[-104.2, -96.47, 45.3, 49.1],
            'sd':[-104.14, -96.3, 42.12, 46.15],
            'ne':[-104.14, -95.25, 39.3, 43.1],
            'md':[-79.52, -74.97, 37.9, 39.79],
            'va':[-83.77, -75.15, 35.7, 39.53],
            'sc':[-83.46, -78.35, 31.4, 35.25],
            'ky':[-89.64, -81.86, 35.8, 39.24],
            'wv':[-82.68, -77.61, 36.5, 40.72],
            'nc':[-84.4, -75.35, 33, 37],
            'nv':[-120.15, -113.92, 34.91, 42.09],
            'fl':[-87.71, -79.77, 24.44, 31.08],
            'or':[-125, -116.25, 41.3, 46.36],
            'wa':[-125, -116.9, 44.8, 49.1],
            'id':[-117.4, -110.97, 41.2, 49.1],
            'ga':[-85.8, -80.68, 29.8, 35.05],
            'al':[-88.75, -84.77, 29.5, 35.05],
            'ms':[-91.82, -87.95, 29.65, 35.05],
            'la':[-94.24, -88.85, 28.4, 33.13],
            'ar':[-94.81, -89.48, 32.4, 36.58],
            'tx':[-106.95, -93.28, 24.9, 36.71],
            'ok':[-103.18, -94.26, 33.5, 37.2],
            'nm':[-109.24, -102.89, 30.3, 37.1],
            'az':[-115.05, -108.94, 30.7, 37.1],
            'ut':[-114.2, -108.97, 36.2, 42.1],
            'co':[-109.2, -101.93, 36.4, 41.1],
            'wy':[-111.1, -103.95, 40.4, 45.07],
            'mt':[-116.22, -103.93, 43.4, 49.1],
            'ks':[-102.16, -94.51, 36.3, 40.11],
            'tn':[-90.37, -81.57, 34.2, 36.75],
            'aicc':[-170, -130, 50, 75],
            'oscc':[-122.1, -113.93, 32.4, 39.06],
            'oncc':[-124.8, -119.1, 35.9, 42.15],
            'gbcc':[-120.5, -107.47, 33, 46.4],
            'nrcc':[-117.7, -96, 41.5, 50],
            'rmcc':[-111.3, -94.2, 35.2, 46.8],
            'swcc':[-114.89, -101.7, 30.2, 38],
            'sacc':[-106.88, -74.7, 23.5, 39.65],
            'eacc':[-97.35, -66.18, 33.5, 49.65],
            'nwcc':[125, -116.25, 41, 49.1],
            'conus & south canada & north mexico':[-140, -45, 20, 65],
            'canada':[-141.5, -51, 41, 85],
            'north america':[-180, -51, 20, 85],
            'asia':[40, 180, 0, 81],
            'south america':[-96, -31, -58, 14],
            'australia & new zealand':[108, 180, -48, -9],
            'east asia':[63, 150, 4.5, 56],
            'southeast asia':[87, 163, -13, 31],
            'middle east':[22, 65, 10, 45],
            'mexico & central america':[-118, -75, 6, 33],
            'caribbean':[-86, -58, 9, 28],
            'india':[67, 90, 5, 36.5],
            'guyana':[-62, -56, 0.5, 9]
        
    }
        
    else:
        
        bounds = {
            
            'custom':[western_bound, eastern_bound, southern_bound, northern_bound]
        }
    
    return bounds[region][0], bounds[region][1], bounds[region][2], bounds[region][3]