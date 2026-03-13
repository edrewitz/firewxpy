"""
This file hosts the functions that import shapefiles/GEOJSON associated with the demarcation system (reference system) on the map.

(C) Eric J. Drewitz 2024-2026
"""


from shapeography import(
    client,
    unzip,
    geometry
)


def import_shapefile_from_web(url,
                                path, 
                                filename, 
                                proxies, 
                                chunk_size,
                                notifications, 
                                refresh,
                                file_extension,
                                file_path,
                                edgecolor):
    
    """
    This function downloads and imports the geometry from a shapefile hosted on the web.
    
    Required Arguments:
    
    1) url (String) - The download URL to the file. 
    
    2) path (String) - The directory where the file is saved to. 
    
    3) filename (String) - The name the user wishes to save the file as. 
    
    4) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
        get_shapefiles(url, path, filename, proxies=proxies)
                        
    5) chunk_size (Integer) - The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    6) notifications (String) - Notification when a file is downloaded and saved to {path}
    
    7) refresh (Boolean) - When set to True, the branch that hosts the shapefiles files is completely
       cleaned out and a new set of shapefiles is downloaded with each run. This is recommended for those using 
       shapeography in automated tasks to account for periodic shapefile updates on the servers that host the shapefiles.
    
    8) file_extension (String) - Default='.zip'. - The extension of the zip file. 
    
        Supported zip file extentions
        -----------------------------
            
            1) .zip
            2) .gz
            3) .tar.gz
            4) .tar
            
    9) file_path (String) - The full filepath to the shapefile. 
    
    10) edgecolor (String) - The color of the bordr demarcations on the map. 
    
    Returns
    -------
    
    The geometry of a shapefile to plot with cartopy.    
    """
    
    client.get_shapefiles(url,
                     path,
                     filename,
                     proxies=proxies,
                     chunk_size=chunk_size,
                     notifications=notifications,
                     refresh=refresh)
    
    unzip.extract_files(path,
                        file_extension=file_extension)
    
    shapes = geometry.cartopy_shapefeature(file_path,
                                           edgecolor=edgecolor)
    
    shapes = shapes.geometries()
    
    return shapes


def import_shapefile_local(file_path,
                                edgecolor):
    
    """
    This function imports a locally hosted shapefile.
    
    Required Arguments:
    
    1) file_path (String) - The full filepath to the shapefile. 
    
    2) edgecolor (String) - The color of the bordr demarcations on the map. 
    
    Returns
    -------
    
    The geometry of a shapefile to plot with cartopy.    
    """
    
    shapes = geometry.cartopy_shapefeature(file_path,
                                           edgecolor=edgecolor)
    
    shapes = shapes.geometries()
    
    return shapes
    
def import_geojson_from_web(url,
                                path, 
                                filename, 
                                proxies, 
                                chunk_size,
                                notifications, 
                                refresh,
                                file_extension,
                                file_path):
    
    """
    This function downloads and imports the geometry from a GEOJSON hosted on the web.
    
    Required Arguments:
    
    1) url (String) - The download URL to the file. 
    
    2) path (String) - The directory where the file is saved to. 
    
    3) filename (String) - The name the user wishes to save the file as. 
    
    4) proxies (dict or None) - If the user is using proxy server(s), the user must change the following:

       proxies=None ---> proxies={
                               'http':'http://your-proxy-address:port',
                               'https':'http://your-proxy-address:port'
                               }
                        
        get_shapefiles(url, path, filename, proxies=proxies)
                        
    5) chunk_size (Integer) - The size of the chunks when writing the GRIB/NETCDF data to a file.
    
    6) notifications (String) - Notification when a file is downloaded and saved to {path}
    
    7) refresh (Boolean) - When set to True, the branch that hosts the GEOJSON files is completely
       cleaned out and a new set of shapefiles is downloaded with each run. This is recommended for those using 
       shapeography in automated tasks to account for periodic GEOJSON updates on the servers that host the GEOJSONs.
    
    8) file_extension (String) - Default='.zip'. - The extension of the zip file. 
    
        Supported zip file extentions
        -----------------------------
            
            1) .zip
            2) .gz
            3) .tar.gz
            4) .tar
            
    9) file_path (String) - The full filepath to the GEOJSON. 
    
    Returns
    -------
    
    The geometry of a GEOJSON to plot with cartopy.    
    """
    
    client.get_shapefiles(url,
                     path,
                     filename,
                     proxies=proxies,
                     chunk_size=chunk_size,
                     notifications=notifications,
                     refresh=refresh)
    
    unzip.extract_files(path,
                        file_extension=file_extension)
    
    shapes = geometry.get_geometries(file_path)
    
    return shapes

def import_geojson_local(file_path):
    
    """
    This function imports the geometry of a locally hosted GEOJSON
    
    Required Arguments:
    
    1) file_path (String) - The full filepath to the GEOJSON. 
    
    Returns
    -------
    
    The geometry of a GEOJSON to plot with cartopy.    
    """
    
    shapes = geometry.get_geometries(file_path)
    
    return shapes