# THIS FILE CONTAINS FUNCTIONS THAT RETURN VARIOUS TYPES OF GEOMETRIES FOR PLOTTING
# PYTHON DEPENDENCIES:
# 1) MATPLOTLIB
# 2) CARTOPY
#
#  (C) METEOROLOGIST ERIC J. DREWITZ
#               USDA/USFS

###### IMPORTS ################
import urllib.request
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import warnings
warnings.filterwarnings('ignore')

from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from firewxpy.utilities import file_functions

def get_shapes(file_path):

    try:
        shape_feature = ShapelyFeature(Reader(file_path).geometries(),
                                       ccrs.PlateCarree(), facecolor=(0,0,0,0), edgecolor='black')

        fname = os.path.basename(file_path)
    
        return shape_feature

    except Exception as a:
        error = shape_file_error()
        print(error)

    
def shape_file_error():
    error_msg = f"""
    
    WARNING: COULD NOT FIND FILE. PLEASE MAKE SURE YOU HAVE THE CORRECT FILE PATH. 

    ALSO, BE SURE TO HAVE ALL THE FILES AS FOLLOWS LOCATED IN THE FOLDER.
    HERE IS AN EXAMPLE WITH USING THE PSA BOUNDARY SHAPE FILES. 

    National_PSA_Current.shp
    National_PSA_Current.shx
    National_PSA_Current.xml
    National_PSA_Current.cpg
    National_PSA_Current.dbf
    National_PSA_Current.prj

    THE .SHP FILE IS THE FILE THAT NEEDS TO BE USED IN THE FUNCTION. 

    """
    return error_msg


def download_shape_files():

    # Defines file paths for different shapefiles
    cwa_path = f"NWS CWA Boundaries"
    fwz_path = f"NWS Fire Weather Zones"
    pz_path = f"NWS Public Zones"
    psa_path = f"PSA Shapefiles"
    gacc_path = f"GACC Boundaries Shapefiles"

    # CWAs
    
    if os.path.exists(cwa_path):
        pass
    else:
        # Makes new folder
        print("Welcome First Time FireWxPy User!\nLet me set you up automatically by downloading & installing all the shapefiles while also building the Weather Data directory for you.\nMy Motto is: 'Let the FireWxPy functions do the work so you don't have to!'\nSetting Up...")
        os.mkdir("NWS CWA Boundaries")
        # Downloads the CWA Shapefiles
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/NWS_CWA_Boundaries/w_05mr24.dbf', 'w_05mr24.dbf')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/firewxpy/refs/heads/main/shapefiles/NWS_CWA_Boundaries/w_05mr24.prj', 'w_05mr24.prj')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/NWS_CWA_Boundaries/w_05mr24.shx', 'w_05mr24.shx')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/NWS_CWA_Boundaries/w_05mr24.zip', 'w_05mr24.zip')
        # Moves files to new folder
        os.replace('w_05mr24.zip', f"NWS CWA Boundaries/w_05mr24.zip")
        os.replace('w_05mr24.dbf', f"NWS CWA Boundaries/w_05mr24.dbf")
        os.replace('w_05mr24.prj', f"NWS CWA Boundaries/w_05mr24.prj")
        os.replace('w_05mr24.shx', f"NWS CWA Boundaries/w_05mr24.shx")

    # Fire Weather Zones

    if os.path.exists(fwz_path):
        pass
    else:
        # Makes new folder
        os.mkdir("NWS Fire Weather Zones")
        # Downloads the FWZ Shapefiles
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/NWS_Fire_Weather_Zones/fz05mr24.zip', 'fz05mr24.zip')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/NWS_Fire_Weather_Zones/fz05mr24.dbf', 'fz05mr24.dbf')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/NWS_Fire_Weather_Zones/fz05mr24.prj', 'fz05mr24.prj')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/NWS_Fire_Weather_Zones/fz05mr24.shx', 'fz05mr24.shx')
        # Moves files to new folder
        os.replace('fz05mr24.zip', f"NWS Fire Weather Zones/fz05mr24.zip")
        os.replace('fz05mr24.dbf', f"NWS Fire Weather Zones/fz05mr24.dbf")
        os.replace('fz05mr24.prj', f"NWS Fire Weather Zones/fz05mr24.prj")
        os.replace('fz05mr24.shx', f"NWS Fire Weather Zones/fz05mr24.shx")

    # Public Zones

    if os.path.exists(pz_path):
        pass
    else:
        # Makes new folder
        os.mkdir("NWS Public Zones")
        # Downloads files
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/NWS_Public_Zones/z_05mr24.zip', 'z_05mr24.zip')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/NWS_Public_Zones/z_05mr24.dbf', 'z_05mr24.dbf')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/NWS_Public_Zones/z_05mr24.prj', 'z_05mr24.prj')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/NWS_Public_Zones/z_05mr24.shx', 'z_05mr24.shx')
        # Moves files to new folder
        os.replace('z_05mr24.zip', f"NWS Public Zones/z_05mr24.zip")
        os.replace('z_05mr24.dbf', f"NWS Public Zones/z_05mr24.dbf")
        os.replace('z_05mr24.prj', f"NWS Public Zones/z_05mr24.prj")
        os.replace('z_05mr24.shx', f"NWS Public Zones/z_05mr24.shx")

    # GACC Boundaries
    if os.path.exists(gacc_path):
        pass
    else:
        # Makes new folder
        os.mkdir("GACC Boundaries Shapefiles")
        # Downloads files
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/GACC%20Boundaries%20Shapefiles/National_GACC_Boundaries.xml', 'National_GACC_Boundaries.xml')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/GACC%20Boundaries%20Shapefiles/National_GACC_Current.cpg', 'National_GACC_Current.cpg')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/GACC%20Boundaries%20Shapefiles/National_GACC_Current.dbf', 'National_GACC_Current.dbf')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/GACC%20Boundaries%20Shapefiles/National_GACC_Current.prj', 'National_GACC_Current.prj')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/GACC%20Boundaries%20Shapefiles/National_GACC_Current.shp', 'National_GACC_Current.shp')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/GACC%20Boundaries%20Shapefiles/National_GACC_Current.shx', 'National_GACC_Current.shx')
        # Moves files to folder
        os.replace('National_GACC_Boundaries.xml', f"GACC Boundaries Shapefiles/National_GACC_Boundaries.xml")
        os.replace('National_GACC_Current.cpg', f"GACC Boundaries Shapefiles/National_GACC_Current.cpg")
        os.replace('National_GACC_Current.dbf', f"GACC Boundaries Shapefiles/National_GACC_Current.dbf")
        os.replace('National_GACC_Current.prj', f"GACC Boundaries Shapefiles/National_GACC_Current.prj")
        os.replace('National_GACC_Current.shp', f"GACC Boundaries Shapefiles/National_GACC_Current.shp")
        os.replace('National_GACC_Current.shx', f"GACC Boundaries Shapefiles/National_GACC_Current.shx")

    # PSA Boundaries
    if os.path.exists(psa_path):
        pass
    else:
        # Makes new folder
        os.mkdir("PSA Shapefiles")
        # Downloads files

        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/PSA%20Shapefiles/National_PSA_Current.xml', 'National_PSA_Current.xml')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/PSA%20Shapefiles/National_PSA_Current.cpg', 'National_PSA_Current.cpg')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/PSA%20Shapefiles/National_PSA_Current.dbf', 'National_PSA_Current.dbf')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/PSA%20Shapefiles/National_PSA_Current.prj', 'National_PSA_Current.prj')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/PSA%20Shapefiles/National_PSA_Current.shp', 'National_PSA_Current.shp')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/edrewitz/FireWxPy/main/shapefiles/PSA%20Shapefiles/National_PSA_Current.shx', 'National_PSA_Current.shx')

        # Moves files to folder
        os.replace('National_PSA_Current.xml', f"PSA Shapefiles/National_PSA_Current.xml")
        os.replace('National_PSA_Current.cpg', f"PSA Shapefiles/National_PSA_Current.cpg")
        os.replace('National_PSA_Current.dbf', f"PSA Shapefiles/National_PSA_Current.dbf")
        os.replace('National_PSA_Current.prj', f"PSA Shapefiles/National_PSA_Current.prj")
        os.replace('National_PSA_Current.shp', f"PSA Shapefiles/National_PSA_Current.shp")
        os.replace('National_PSA_Current.shx', f"PSA Shapefiles/National_PSA_Current.shx")
        print("Set Up Complete! Have Fun!")



def import_shapefiles(file_path, line_color, boundary_type):

    r'''
    This function reads and returns the shapefiles (.shp) files from a specific file location. 

    Required Arguments: 1) file_path (String) - The file location of the SHP files. 
                        2) line_color (String) - The color the user wishes to display for the borders in the shapefile. 
                        3) boundary_type (String) - The type of geographical boundaries the user wishes to use. 
                                                    This is necessary because the NWS boundaries have a large file size which to be able to host on github, the files need to be zipped so we need to unzip and extract those files. 

    Returns: 1) The shapefile borders the user wishes to import into the weather graphics. 

    '''
    file_path = file_path 
    line_color = line_color
    boundary_type = boundary_type

    download_shape_files()

    if boundary_type == 'cwa':

        if os.path.exists(f"NWS CWA Boundaries/w_05mr24.shp"):
            pass
        else:
            file_functions.extract_zipped_files(f"NWS CWA Boundaries/w_05mr24.zip", f"NWS CWA Boundaries")

    elif boundary_type == 'fwz':

        if os.path.exists(f"NWS Fire Weather Zones/fz05mr24.shp"):
            pass
        else:
            file_functions.extract_zipped_files(f"NWS Fire Weather Zones/fz05mr24.zip", f"NWS Fire Weather Zones")

    elif boundary_type == 'pz':

        if os.path.exists(f"NWS Public Zones/z_05mr24.shp"):
            pass
        else:
            file_functions.extract_zipped_files(f"NWS Public Zones/z_05mr24.zip", f"NWS Public Zones")

    else:
        pass

PSAs = import_shapefiles(f"PSA Shapefiles/National_PSA_Current.shp", 'black', 'psa')

GACC = import_shapefiles(f"GACC Boundaries Shapefiles/National_GACC_Current.shp", 'black', 'gacc')

CWAs = import_shapefiles(f"NWS CWA Boundaries/w_05mr24.shp", 'black', 'cwa')

FWZs = import_shapefiles(f"NWS Fire Weather Zones/fz05mr24.shp", 'black', 'fwz')

PZs = import_shapefiles(f"NWS Public Zones/z_05mr24.shp", 'black', 'pz')

