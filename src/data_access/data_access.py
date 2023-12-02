# THIS SCRIPT HAS FUNCTIONS THAT DOWNLOAD FORECAST DATA FROM THE NOAA/NWS FTP SERVER, ORGANIZE THE GRIB FILES AND RETURN BOOLEAN VALUES DEPENDING ON IF THE GRIB FILE EXISTS OR NOT
#
# THIS IS THE NWS FTP DATA ACCESS FILE FOR FIREPY
#
# THIS SCRIPT ALSO ACCESSES THE LATEST 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATA (RTMA DATA) FROM THE UCAR THREDDS SERVER. RTMA DATA IS USEFUL FOR REAL-TIME ANALYSIS PLOTTING
#
#
# DEPENDENCIES INCLUDE:
# 1. PYGRIB
# 2. XARRAY
# 3. OS
# 4. FTPLIB
# 5. DATETIME
# 6. SIPHON
# 7. METPY
#
#  (C) METEOROLOGIST ERIC J. DREWITZ
#               USDA/USFS

##### IMPORTS NEEDED PYTHON MODULES #######
import pygrib
import xarray as xr
import os
import metpy
import metpy.calc as mpcalc

from ftplib import FTP
from datetime import datetime, timedelta
from siphon.catalog import TDSCatalog


def directory_name_error():
    error_msg = f"""

    WARNING: USER ENTERED AN INVALID DIRECTORY NAME

    HERE IS THE URL FOR THE NOAA/NWS FTP SERVER WEBSITE: https://tgftp.nws.noaa.gov/

    HERE IS THE LIST OF VALID DIRECTORY NAMES ***NOTE USER STILL NEEDS TO ENTER THE LAST PORTION OF THE DIRECTORY NAME***
    
    AN EXAMPLE OF THE LAST PORTION OF A DIRECTORY NAME IS AS FOLLOWS: /VP.001-003/

    FULL DIRECTORY NAME LIST:

    ALASKA: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/
    CONUS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/
    CENTRAL GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crgrlake/
    CENTRAL MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/
    CENTRAL PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/
    CENTRAL ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/
    EASTERN GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.ergrlake/
    GUAM: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.guam/
    HAWAII: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/
    MID-ATLANTIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/
    NORTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/
    NORTHERN HEMISPHERE: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nhemi/
    NORTH PACIFIC OCEAN: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.npacocn/
    NORTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/
    NORTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/
    OCEANIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.oceanic/
    PACIFIC NORTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/
    PACIFIC SOUTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
    PUERTO RICO: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.puertori/
    SOUTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/
    SOUTHERN MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/
    SOUTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/
    SOUTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.srockies/
    UPPER MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/
    
    """
    print(error_msg)

def directory_list():
    dir_list = f"""
    
    FULL DIRECTORY NAME LIST:
        
    ALASKA: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.alaska/
    CONUS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.conus/
    CENTRAL GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crgrlake/
    CENTRAL MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crmissvy/
    CENTRAL PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crplains/
    CENTRAL ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.crrocks/
    EASTERN GREAT LAKES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.ergrlake/
    GUAM: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.guam/
    HAWAII: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.hawaii/
    MID-ATLANTIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.midatlan/
    NORTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.neast/
    NORTHERN HEMISPHERE: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nhemi/
    NORTH PACIFIC OCEAN: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.npacocn/
    NORTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nplains/
    NORTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.nrockies/
    OCEANIC: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.oceanic/
    PACIFIC NORTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacnwest/
    PACIFIC SOUTHWEST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.pacswest/
    PUERTO RICO: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.puertori/
    SOUTHEAST: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.seast/
    SOUTHERN MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.smissvly/
    SOUTHERN PLAINS: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.splains/
    SOUTHERN ROCKIES: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.srockies/
    UPPER MISSISSIPPI VALLEY: /SL.us008001/ST.opnl/DF.gr2/DC.ndfd/AR.umissvly/
    
    """
    print(dir_list)


def parameter_name_error():
    error_msg = f"""

    WARNING: USER ENTERED AN INVALID PARAMETER NAME. 

    FOR THE FULL LIST OF PARAMETER NAMES VISIT THE FOLLOWING LINK:

    https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK

    """
    print(error_msg)


def parameter_list():
    param_list = f"""

    FOR THE FULL LIST OF PARAMETERS, PLEASE VISIT THE FOLLOWING LINK:

    https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK

    """
    print(param_list)
    

def get_NWS_NDFD_grid_data(directory_name, parameter):
    
    r'''
    THIS FUNCTION DOWNLOADS FORECAST DATA FROM THE NOAA/NWS FTP SERVER. 

    THE USER NEEDS TO ENTER THE NAME OF THE DIRECTORY IN WHICH THE USER NEEDS DATA FROM AS WELL AS THE PARAMETER

    FOR THE FULL LIST OF THE VARIOUS PARAMETERS PLEASE REFER TO: 

    https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK

    COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
    '''

    ###################################################
    # NDFD GRIDS DATA ACCESS FROM NOAA/NWS FTP SERVER #
    ###################################################

    ### CONNECTS TO THE NOAA/NWS FTP SERVER ###
    ftp = FTP('tgftp.nws.noaa.gov')
    ftp.login()

    ### SEARCHES FOR THE CORRECT DIRECTORY ###
    try:
        dirName = directory_name
        param = parameter
        files = ftp.cwd(dirName)

        ### SEARCHES FOR THE CORRECT PARAMETER ###
        try:
            ################################
            # DOWNLOADS THE NWS NDFD GRIDS #
            ################################
            
            with open(param, 'wb') as fp:
                ftp.retrbinary('RETR ' + param, fp.write)    
            
            ftp.close()
            
            #########################
            # DATA ARRAYS PARAMETER #
            #########################
            
            ds = xr.load_dataset(param, engine='cfgrib')
            grbs = pygrib.open(param)
            grbs.seek(0)
            return grbs

        ### ERROR MESSAGE WHEN THERE IS AN INVALID PARAMETER NAME ###

        except Exception as a:
            param_error = parameter_name_error()
            return param_error

    ### ERROR MESSAGE WHEN THERE IS AN INVALID DIRECTORY NAME ###
        
    except Exception as e:
        dir_error = directory_name_error()
        return dir_error



def sort_GRIB_files(GRIB_File_List, parameter):
    
    r'''
    THIS FUNCTION SORTS AND RETURNS THE INDIVIDUAL GRIB FILES IN THE DOWNLOADED DATASET. 

    THIS FUNCTION ALSO RETURNS THE COUNT OF THE NUMBER OF GRIB FILES IN THE DATASET.

    THIS FUNCTION IS TO BE USED IN THE PROGRAMMER'S CODE AFTER THE get_NWS_NDFD_grid_data(directory_name, parameter) FUNCTION IS USED

    COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
    '''
    count = 0
    for grb in GRIB_File_List:
        count = count + 1
    if count == 1:
        grb_1 = GRIB_File_List[1]
        grb_2 = None
        grb_3 = None
        grb_4 = None
        grb_5 = None
    
    if count == 2:
        grb_1 = GRIB_File_List[1]
        grb_2 = GRIB_File_List[2]
        grb_3 = None
        grb_4 = None
        grb_5 = None
        
    if count == 3: 
        grb_1 = GRIB_File_List[1]
        grb_2 = GRIB_File_List[2]
        grb_3 = GRIB_File_List[3]
        grb_4 = None
        grb_5 = None
    
    if count == 4: 
        grb_1 = GRIB_File_List[1]
        grb_2 = GRIB_File_List[2]
        grb_3 = GRIB_File_List[3]
        grb_4 = GRIB_File_List[4]
        grb_5 = None

    if count >= 5: 
        grb_1 = GRIB_File_List[1]
        grb_2 = GRIB_File_List[2]
        grb_3 = GRIB_File_List[3]
        grb_4 = GRIB_File_List[4]
        grb_5 = GRIB_File_List[5]

    print("There are " + str(count) + " GRIB files in the " + parameter + " download.")
    return grb_1, grb_2, grb_3, grb_4, grb_5, count


def GRIB_file_checker(GRIB_File_List):
    
    r'''
    THIS FUNCTION IS USEFUL WHEN HAVING AUTOMATED DISPLAYS OF THE VARIOUS GRIB FILE DATA

    THIS FUNCTION CHECKS TO SEE HOW MANY GRIB FILES ARE RETURNED IN THE LIST WHICH IS HELPFUL FOR GRAPHICS

    THIS FUNCTION IS TO BE USED IN THE PROGRAMMER'S CODE AFTER THE get_NWS_NDFD_grid_data(directory_name, parameter) FUNCTION IS USED

    THIS FUNCTION WILL RETURN A BOOLEAN VALUE FOR IF OR IF NOT THE FILE EXISTS

    USUALLY THERE ARE NOT MORE THAN 5 GRIB FILES IN A DOWNLOAD AT A TIME

    IF THE GRIB FILE EXISTS, A BOOLEAN VALUE OF TRUE IS RETURNED AND IF THE GRIB FILE DOESN'T EXIST A BOOLEAN VALUE OF FALSE IS RETURNED. 

    THE LOGICAL CHECKS HELPS WHEN THE USER IS MAKING AUTOMATED GRAPHICS TO MAKE SURE THE NUMBER OF SUBPLOTS IS EQUAL TO THE NUMBER OF GRIB FILES

    THIS FUNCTION ALSO RETURNS THE COUNT OF THE NUMBER OF GRIB FILES IN THE DATASET.

    COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
    '''
    count = 0
    for grb in GRIB_File_List:
        count = count + 1
    if count == 1:
        grb_1_logic = True
        grb_2_logic = False
        grb_3_logic = False
        grb_4_logic = False
        grb_5_logic = False
    
    if count == 2:
        grb_1_logic = True
        grb_2_logic = True
        grb_3_logic = False
        grb_4_logic = False
        grb_5_logic = False
        
    if count == 3: 
        grb_1_logic = True
        grb_2_logic = True
        grb_3_logic = True
        grb_4_logic = False
        grb_5_logic = False
    
    if count == 4: 
        grb_1_logic = True
        grb_2_logic = True
        grb_3_logic = True
        grb_4_logic = True
        grb_5_logic = False

    if count >= 5: 
        grb_1_logic = True
        grb_2_logic = True
        grb_3_logic = True
        grb_4_logic = True
        grb_5_logic = True

    return grb_1_logic, grb_2_logic, grb_3_logic, grb_4_logic, grb_5_logic, count



def get_GRIB_file_values(GRIB_File):
 
    r'''
    THIS FUNCTION RETURNS THE VALUES OF THE DATA INSIDE OF A GRIB FILE. 

    COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
    '''
    return GRIB_File.values


def get_GRIB_file_valid_date(GRIB_File):

    r'''
    THIS FUNCTION RETURNS THE VALID DATE FOR A GRIB FILE

    COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
    '''
    return GRIB_File.validDate


def NDFD_Forecast_Time_Interval(GRIB_File, hours): 
   
    r'''
    THIS FUNCTION WILL RETURN THE TIME THE FORECAST PERIOD ENDS BASED ON HOW LONG THE FORECAST PERIOD IS VALID FOR
    THE VALID DATE FOR A GRIB FILE CORRESPONDS TO THE START OF THE FORECAST PERIOD. 
    (I.E. THE NDFD MAXIMUM RELATIVE HUMIDITY GRIDS ARE A TIME LENGTH OF 12HRS, THEREFORE THE ENDING TIME OF THE FORECAST PERIOD IS 12HRS AFTER THE VALID DATE OF THE GRIB FILE. 

    PYTHON MODULE DEPENDENCIES:
    1. DATETIME

    COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023
    '''

    return GRIB_File.validDate + timedelta(hours=hours)
        










def syntax_error():
    error_msg = f"""

    WARNING: DATA COULD NOT BE RETRIEVED. 

    THIS IS DUE TO A LIKELY SYNTAX ERROR. 

    THIS IS MOST LIKELY DUE TO THE PARAMETER BEING DEFINED WITH INCORRECT SYNTAX

    FOR THE FULL OPENDAP LIST OF PARAMETERS FOR REAL TIME MESOSCALE ANALYSIS DATA VISIT

    https://thredds.ucar.edu/thredds/dodsC/grib/NCEP/RTMA/CONUS_2p5km/Best.html

    """

    print(error_msg)


def get_current_rtma_data(current_time, parameter):

    r"""
    THIS FUNCTION RETRIEVES THE LATEST 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATASET FOR A PARAMETER SPECIFIED BY THE USER

    IF THE DATASET FOR THE CURRENT TIME IS UNAVAILABLE THE FUNCTION WILL TRY TO RETURN THE MOST RECENT DATASET IN THE PAST 4 HOURS

    IF THE USER HAS A SYNTAX ERROR THE LINK TO THE UCAR THREDDS OPENDAP PARAMETER LIST WILL BE DISPLAYED

    PYTHON PACKAGE DEPENDENCIES:

    1. SIPHON
    2. METPY
    3. DATETIME

    RETURNS:

    CURRENT RTMA DATASET FOR THE PARAMETER DEFINED BY THE USER

    COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023

    """

    times = []

    for i in range(1,5):
        new_time = current_time - timedelta(hours=i)
        times.append(new_time)

    try:
        rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+current_time.strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+current_time.strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
        rtma_data = rtma_data.metpy.parse_cf()
        rtma_parameter = rtma_data[parameter].squeeze()
        print("Data retrieval for " + current_time.strftime('%m/%d/%Y %H00 UTC') + " is successful")
        
        return rtma_parameter
        
    except Exception as e:

        print(parameter + " Data is unavailiable for "+current_time.strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[0].strftime('%m/%d/%Y %H00 UTC'))
        
        try:
            rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf()
            rtma_parameter = rtma_data[parameter].squeeze()

            print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")
            return rtma_parameter

        except Exception as a:

            print(parameter + " Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC'))
           
            try:
                rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf()
                rtma_parameter = rtma_data[parameter].squeeze()
    
                print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                return rtma_parameter


            except Exception as b:
                            
                print(parameter + " Data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC'))

                try:
                    rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf()
                    rtma_parameter = rtma_data[parameter].squeeze()
    
                    print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                    return rtma_parameter

                except Exception as c:
                            
                    print(parameter + " Data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC'))

                    try:
                        rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf()
                        rtma_parameter = rtma_data[parameter].squeeze()
        
                        print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                        return rtma_parameter
                    
                
                    except syntaxError as k:
                        error = syntax_error()

                        return error


def get_rtma_data_24_hour_difference(current_time, parameter):

    r"""
    THIS FUNCTION RETRIEVES THE LATEST 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATASET FOR A PARAMETER SPECIFIED BY THE USER

    THIS FUNCTION ALSO RETRIEVES THE DATASET FROM 24 HOURS PRIOR TO THE CURRENT DATASET FOR A 24 HOUR COMPARISON

    THE 24 HOUR COMPARISON IS SUBTRACTING THE CURRENT VALUES FROM THE VALUES FROM 24 HOURS AGO TO SHOW THE CHANGE
    
    PYTHON PACKAGE DEPENDENCIES:

    1. SIPHON
    2. METPY
    3. DATETIME

    RETURNS:

    THE DIFFERENCE IN VALUES BETWEEN THE CURRENT DATASET AND DATASET FROM 24 HOURS AGO FOR THE PARAMETER DEFINED BY THE USER

    COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023

    """

    times = []
    times_24 = []

    for i in range(0,5):
        new_time = current_time - timedelta(hours=i)
        old_time = new_time - timedelta(hours=24)
        times.append(new_time)
        times_24.append(old_time)
        
    try:
        rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
        rtma_data = rtma_data.metpy.parse_cf()
        rtma_parameter = rtma_data[parameter].squeeze()

        rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
        rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
        rtma_data_24 = rtma_data_24.metpy.parse_cf()
        rtma_parameter_24 = rtma_data_24[parameter].squeeze()

        print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")
        
        return rtma_parameter - rtma_parameter_24
        
    except Exception as e:
        
        print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " and/or " + times_24[0].strftime('%m/%d/%Y %H00 UTC') + " is unsuccessful")
        print("Will try to download the most recent datasets from "+times[1].strftime('%m/%d/%Y %H00 UTC')+ " and " + times_24[1].strftime('%m/%d/%Y %H00 UTC'))
        
        try:
            rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf()
            rtma_parameter = rtma_data[parameter].squeeze()
    
            rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data_24 = rtma_data_24.metpy.parse_cf()
            rtma_parameter_24 = rtma_data_24[parameter].squeeze()
    
            print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")
            
            return rtma_parameter - rtma_parameter_24
     
        except Exception as a:

            print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " and/or " + times_24[1].strftime('%m/%d/%Y %H00 UTC') + " is unsuccessful")
            print("Will try to download the most recent datasets from "+times[2].strftime('%m/%d/%Y %H00 UTC')+ " and " + times_24[2].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf()
                rtma_parameter = rtma_data[parameter].squeeze()
        
                rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data_24 = rtma_data_24.metpy.parse_cf()
                rtma_parameter_24 = rtma_data_24[parameter].squeeze()
        
                print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                
                return rtma_parameter - rtma_parameter_24


            except Exception as b:
                            
                print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " and/or " + times_24[2].strftime('%m/%d/%Y %H00 UTC') + " is unsuccessful")
                print("Will try to download the most recent datasets from "+times[3].strftime('%m/%d/%Y %H00 UTC')+ " and " + times_24[3].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf()
                    rtma_parameter = rtma_data[parameter].squeeze()
            
                    rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data_24 = rtma_data_24.metpy.parse_cf()
                    rtma_parameter_24 = rtma_data_24[parameter].squeeze()
            
                    print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                    
                    return rtma_parameter - rtma_parameter_24

                except Exception as c:
                            
                    print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " and/or " + times_24[3].strftime('%m/%d/%Y %H00 UTC') + " is unsuccessful")
                    print("Will try to download the most recent datasets from "+times[4].strftime('%m/%d/%Y %H00 UTC')+ " and " + times_24[4].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf()
                        rtma_parameter = rtma_data[parameter].squeeze()
                
                        rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data_24 = rtma_data_24.metpy.parse_cf()
                        rtma_parameter_24 = rtma_data_24[parameter].squeeze()
                
                        print("Data retrieval for " + times[4].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                        
                        return rtma_parameter - rtma_parameter_24
                              
                
                    except syntaxError as k:
                        error = syntax_error()

                        return error


def get_current_rtma_relative_humidity_data(current_time):

    r"""
    THIS FUNCTION RETRIEVES THE LATEST 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATASETS FOR TEMPERATURE AND DEWPOINT

    THIS FUNCTION THEN CALCULATES A RELATIVE HUMIDITY DATASET USING METPY.CALC FROM THE TEMPERATURE AND DEWPOINT DATASETS

    IF THE DATASET FOR THE CURRENT TIME IS UNAVAILABLE THE FUNCTION WILL TRY TO RETURN THE MOST RECENT DATASET IN THE PAST 4 HOURS

    PYTHON PACKAGE DEPENDENCIES:

    1. SIPHON
    2. METPY
    3. DATETIME

    RETURNS:

    CURRENT RTMA DATASET FOR RELATIVE HUMIDITY

    COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023

    """

    times = []

    for i in range(0,5):
        new_time = current_time - timedelta(hours=i)
        times.append(new_time)

    try:
        rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
        rtma_data = rtma_data.metpy.parse_cf()
        rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
        rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()

        rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
        print("Data retrieval for " + times[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")
        
        return rtma_rh *100
        
    except Exception as e:

        print("Relative Humidity Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC'))
        
        try:
            rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf()
            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
    
            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
            print("Data retrieval for " + times[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")
            
            return rtma_rh *100
  
        except Exception as a:

            print("Relative Humidity data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf()
                rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
        
                rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                print("Data retrieval for " + times[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                
                return rtma_rh *100

            except Exception as b:
                            
                print("Relative Humidity data is unavailiable for "+times[2].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf()
                    rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                    print("Data retrieval for " + times[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                    
                    return rtma_rh *100

                except Exception as c:
                            
                    print("Relative Humidity data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ "\nWill try to download the most recent dataset from "+times[4].strftime('%m/%d/%Y %H00 UTC'))
                    
                    try:
                        rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf()
                        rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                        print("Data retrieval for " + times[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                        
                        return rtma_rh *100
                               
                
                    except Exception as k:
                        print("WARNING: Latest dataset is more than 4 hours old.\nQuitting - Please try again later.")

                        return None


def get_rtma_relative_humidity_24_hour_difference_data(current_time):

    r"""
    THIS FUNCTION RETRIEVES THE LATEST 2.5KM X 2.5KM REAL TIME MESOSCALE ANALYSIS DATASETS FOR TEMPERATURE AND DEWPOINT AND THE CORRESPONDING DATASETS FROM 24 HOURS AGO

    THIS FUNCTION THEN CALCULATES A RELATIVE HUMIDITY DATASET USING METPY.CALC FROM THE TEMPERATURE AND DEWPOINT DATASETS

    IF THE DATASET FOR THE CURRENT TIME IS UNAVAILABLE THE FUNCTION WILL SEARCH FOR THE LATEST DATASET IN THE PAST 4 HOURS

    PYTHON PACKAGE DEPENDENCIES:

    1. SIPHON
    2. METPY
    3. DATETIME

    RETURNS:

    24 HOUR DIFFERENCE IN RELATIVE HUMIDITY

    COPYRIGHT (C) METEOROLOGIST ERIC J. DREWITZ 2023

    """

    times = []
    times_24 = []

    for i in range(0,5):
        new_time = current_time - timedelta(hours=i)
        old_time = new_time - timedelta(hours=24)
        times.append(new_time)
        times_24.append(old_time)

    try:
        rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
        rtma_data = rtma_data.metpy.parse_cf()
        rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
        rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()

        rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)

        rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[0].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
        rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[0].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
        rtma_data_24 = rtma_data_24.metpy.parse_cf()
        rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
        rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()

        rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
        print("Data retrieval for both " + times[0].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[0].strftime('%m/%d/%Y %H00 UTC') + " is successful")
        
        return (rtma_rh - rtma_rh_24) *100
        
    except Exception as e:

        print("Relative Humidity Data is unavailiable for "+times[0].strftime('%m/%d/%Y %H00 UTC')+ " and/or " +times_24[0].strftime('%m/%d/%Y %H00 UTC')+"\nWill try to download the most recent dataset from "+times[1].strftime('%m/%d/%Y %H00 UTC') + " and " +times_24[1].strftime('%m/%d/%Y %H00 UTC'))
        
        try:
            rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data = rtma_data.metpy.parse_cf()
            rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
    
            rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
    
            rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[1].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
            rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[1].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
            rtma_data_24 = rtma_data_24.metpy.parse_cf()
            rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
            rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
    
            rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
            print("Data retrieval for both " + times[1].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[1].strftime('%m/%d/%Y %H00 UTC') + " is successful")
            
            return (rtma_rh - rtma_rh_24) *100 
            
        except Exception as a:

            print("Relative Humidity Data is unavailiable for "+times[1].strftime('%m/%d/%Y %H00 UTC')+ " and/or " +times_24[1].strftime('%m/%d/%Y %H00 UTC')+"\nWill try to download the most recent dataset from "+times[2].strftime('%m/%d/%Y %H00 UTC') + " and " +times_24[2].strftime('%m/%d/%Y %H00 UTC'))
            
            try:
                rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data = rtma_data.metpy.parse_cf()
                rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
        
                rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
        
                rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[2].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[2].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                rtma_data_24 = rtma_data_24.metpy.parse_cf()
                rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
                rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
        
                rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
                print("Data retrieval for both " + times[2].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[2].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                
                return (rtma_rh - rtma_rh_24) *100 
                
            except Exception as b:
                            
                print("Relative Humidity Data is unavailiable for "+times[2].strftime('%m/%d/%Y %H00 UTC')+ " and/or " +times_24[2].strftime('%m/%d/%Y %H00 UTC')+"\nWill try to download the most recent dataset from "+times[3].strftime('%m/%d/%Y %H00 UTC') + " and " +times_24[3].strftime('%m/%d/%Y %H00 UTC'))
                
                try:
                    rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data = rtma_data.metpy.parse_cf()
                    rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
            
                    rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[3].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                    rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[3].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                    rtma_data_24 = rtma_data_24.metpy.parse_cf()
                    rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
                    rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
            
                    rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
                    print("Data retrieval for both " + times[3].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[3].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                    
                    return (rtma_rh - rtma_rh_24) *100 
 
                except Exception as c:
                            
                    print("Relative Humidity Data is unavailiable for "+times[3].strftime('%m/%d/%Y %H00 UTC')+ " and/or " +times_24[3].strftime('%m/%d/%Y %H00 UTC')+"\nWill try to download the most recent dataset from "+times[4].strftime('%m/%d/%Y %H00 UTC') + " and " +times_24[4].strftime('%m/%d/%Y %H00 UTC'))
            
                    try:
                        rtma_cat = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data = rtma_cat.datasets['RTMA_CONUS_2p5km_'+times[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data = rtma_data.metpy.parse_cf()
                        rtma_temp = rtma_data['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt = rtma_data['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh = mpcalc.relative_humidity_from_dewpoint(rtma_temp, rtma_dwpt)
                
                        rtma_cat_24 = TDSCatalog('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/RTMA/CONUS_2p5km/RTMA_CONUS_2p5km_'+times_24[4].strftime('%Y%m%d_%H00')+'.grib2/catalog.xml')
                        rtma_data_24 = rtma_cat_24.datasets['RTMA_CONUS_2p5km_'+times_24[4].strftime('%Y%m%d_%H00')+'.grib2'].remote_access(use_xarray=True)
                        rtma_data_24 = rtma_data_24.metpy.parse_cf()
                        rtma_temp_24 = rtma_data_24['Temperature_Analysis_height_above_ground'].squeeze()
                        rtma_dwpt_24 = rtma_data_24['Dewpoint_temperature_Analysis_height_above_ground'].squeeze()
                
                        rtma_rh_24 = mpcalc.relative_humidity_from_dewpoint(rtma_temp_24, rtma_dwpt_24)
                        print("Data retrieval for both " + times[4].strftime('%m/%d/%Y %H00 UTC') + " and " + times_24[4].strftime('%m/%d/%Y %H00 UTC') + " is successful")
                        
                        return (rtma_rh - rtma_rh_24) *100 
        
                    except Exception as k:
                        print("WARNING: Latest dataset is more than 4 hours old.\nQuitting - Please try again later.")

                        return None

