"""
This class hosts functions to access observational data

(C) Eric J. Drewitz 2025
"""
import firewxpy.utils.parsers as parsers
import pandas as pd
import requests
import firewxpy.utils.calc as calc
import urllib.request
import os
import firewxpy.utils.standard as standard
import warnings
warnings.filterwarnings('ignore')

from siphon.catalog import TDSCatalog
from metpy.cbook import get_test_data
from io import StringIO
from metpy.io import parse_metar_file
from metpy.units import units, pandas_dataframe_to_unit_arrays
from dateutil import tz

try:
    from datetime import datetime, timedelta, UTC
except Exception as e:
    from datetime import datetime, timedelta

def station_coords(station_id):

    """
    This function returns the latitude and lonigitude coordinates for any airport. 

    Required Arguments:

    1) station_id (String) - The ID for the ASOS station. 

    Returns: The latitude/longitude coordinates of the ASOS station in decimal degrees.

    """

    station_id = station_id.upper()
    
    # Pings server for airport data
    df = pd.read_csv(get_test_data('airport-codes.csv'))
    
    # Queries our airport types (airport sizes)
    df = df[(df['type'] == 'large_airport') | (df['type'] == 'medium_airport') | (df['type'] == 'small_airport')]

    df = df[df['ident'] == station_id]

    longitude = df['longitude_deg']
    latitude = df['latitude_deg']

    longitude = longitude.iloc[0]
    latitude = latitude.iloc[0]
    
    return longitude, latitude   

def get_metar_data():

    """
    This function downloads and returns the latest METAR data. 
    
    Inputs: None 

    Returns: 
    
    1) df (Pandas DataFrame) - DataFrame of the latest METAR data
    
    2) time (datetime) - The time of the latest METAR dataset 
    """

    main_server_response = requests.get("https://thredds.ucar.edu/thredds/catalog/catalog.xml")
    backup_server_response = requests.get("https://thredds-dev.unidata.ucar.edu/thredds/catalog/catalog.xml")
    main_server_status = main_server_response.status_code
    backup_server_status = backup_server_response.status_code
    
    # Pings server for airport data
    airports_df = pd.read_csv(get_test_data('airport-codes.csv'))
    
    # Queries our airport types (airport sizes)
    airports_df = airports_df[(airports_df['type'] == 'large_airport') | (airports_df['type'] == 'medium_airport') | (airports_df['type'] == 'small_airport')]
    
    # Accesses the METAR data

    if main_server_status == 200:
        
        try:
            metar_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.xml')

        
        except Exception as e:
            metar_cat = TDSCatalog('https://thredds-test.unidata.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.xml')

    if main_server_status != 200 and backup_server_status == 200:
        try:
            metar_cat = TDSCatalog('https://thredds-dev.unidata.ucar.edu/thredds/catalog/noaaport/text/metar/catalog.xml')

            print("Successfully connected to the backup server! Downloading Data...")
        
        except Exception as e:
            print("ERROR! Cannot connect to either the main or backup server. Aborting!")

    if main_server_status != 200 and backup_server_status != 200:
        print("ERROR! Cannot connect to either the main or backup server. Aborting!")

    ds = metar_cat.datasets[-5]

    if os.path.exists(f"METAR Data"):
        pass
    else:
        os.mkdir(f"METAR Data")

    for file in os.listdir(f"METAR Data"):
        try:
            os.remove(f"METAR Data/{file}")
        except Exception as e:
            pass

    ds.download()
    os.replace(ds.name, f"METAR Data/{ds.name}")
    file_size = (os.path.getsize(f"METAR Data/{ds.name}")/1000000)

    if file_size < 1.2:
        os.remove(f"METAR Data/{ds.name}")
        ds = metar_cat.datasets[-6]
        ds.download()
        os.replace(ds.name, f"METAR Data/{ds.name}")
    else:
        pass
    
    df = parse_metar_file(f"METAR Data/{ds.name}")
    name = os.path.basename(f"METAR Data/{ds.name}")
    year = f"{name[6]}{name[7]}{name[8]}{name[9]}"
    month = f"{name[10]}{name[11]}"
    day = f"{name[12]}{name[13]}"
    hour = f"{name[15]}{name[16]}"

    time = datetime(int(year), int(month), int(day), int(hour))

    df = df.dropna(subset=['latitude', 'longitude', 'air_temperature', 'dew_point_temperature', 'cloud_coverage', 'eastward_wind', 'northward_wind'])
    
    return df, time