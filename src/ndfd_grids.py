# THIS SCRIPT DOWNLOADS FORECAST DATA FROM THE NOAA/NWS FTP SERVER
#
# THIS IS THE NWS FTP DATA ACCESS FILE FOR FIREPY
#
# DEPENDENCIES INCLUDE:
# 1. PYGRIB
# 2. XARRAY
# 3. OS
# 4. FTPLIB
#
#  (C) ERIC J. DREWITZ
#       METEOROLOGIST
#         USDA/USFS

##### IMPORTS NEEDED PYTHON MODULES #######
import pygrib
import xarray as xr
import os
from ftplib import FTP


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
    '''
    THIS FUNCTION DOWNLOADS FORECAST DATA FROM THE NOAA/NWS FTP SERVER. 

    THE USER NEEDS TO ENTER THE NAME OF THE DIRECTORY IN WHICH THE USER NEEDS DATA FROM AS WELL AS THE PARAMETER

    FOR THE FULL LIST OF THE VARIOUS PARAMETERS PLEASE REFER TO: 

    https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.weather.gov%2Fmedia%2Fmdl%2Fndfd%2FNDFDelem_fullres.xls&wdOrigin=BROWSELINK

    COPYRIGHT (C) ERIC J. DREWITZ 2023
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



def GRIB_file_checker(GRIB_File_List):
    '''
    THIS FUNCTION IS USEFUL WHEN HAVING AUTOMATED DISPLAYS OF THE VARIOUS GRIB FILE DATA

    THIS FUNCTION CHECKS TO SEE HOW MANY GRIB FILES ARE RETURNED IN THE LIST WHICH IS HELPFUL FOR GRAPHICS

    THIS FUNCTION IS TO BE USED IN THE PROGRAMMER'S CODE AFTER THE get_NWS_NDFD_grid_data(directory_name, parameter) FUNCTION IS USED

    THIS FUNCTION WILL RETURN EACH INDIVIDUAL GRIB FILE WITH A LOGIC CHECK ASSOCIATED WITH THE GRIB FILES

    USUALLY THERE ARE NOT MORE THAN 5 GRIB FILES IN A DOWNLOAD AT A TIME

    IF THE GRIB FILE EXISTS, A BOOLEAN VALUE OF TRUE IS RETURNED AND IF THE GRIB FILE DOESN'T EXIST A BOOLEAN VALUE OF FALSE IS RETURNED. 

    THE LOGICAL CHECKS HELPS WHEN THE USER IS MAKING AUTOMATED GRAPHICS TO MAKE SURE THE NUMBER OF SUBPLOTS IS EQUAL TO THE NUMBER OF GRIB FILES

    COPYRIGHT (C) ERIC J. DREWITZ 2023
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
        grb_1_logic = True
        grb_2_logic = False
        grb_3_logic = False
        grb_4_logic = False
        grb_5_logic = False
    
    if count == 2:
        grb_1 = GRIB_File_List[1]
        grb_2 = GRIB_File_List[2]
        grb_3 = None
        grb_4 = None
        grb_5 = None
        grb_1_logic = True
        grb_2_logic = True
        grb_3_logic = False
        grb_4_logic = False
        grb_5_logic = False
        
    if count == 3: 
        grb_1 = GRIB_File_List[1]
        grb_2 = GRIB_File_List[2]
        grb_3 = GRIB_File_List[3]
        grb_4 = None
        grb_5 = None
        grb_1_logic = True
        grb_2_logic = True
        grb_3_logic = True
        grb_4_logic = False
        grb_5_logic = False
    
    if count == 4: 
        grb_1 = GRIB_File_List[1]
        grb_2 = GRIB_File_List[2]
        grb_3 = GRIB_File_List[3]
        grb_4 = GRIB_File_List[4]
        grb_5 = None
        grb_1_logic = True
        grb_2_logic = True
        grb_3_logic = True
        grb_4_logic = True
        grb_5_logic = False

    if count >= 5: 
        grb_1 = GRIB_File_List[1]
        grb_2 = GRIB_File_List[2]
        grb_3 = GRIB_File_List[3]
        grb_4 = GRIB_File_List[4]
        grb_5 = GRIB_File_List[5]
        grb_1_logic = True
        grb_2_logic = True
        grb_3_logic = True
        grb_4_logic = True
        grb_5_logic = True

    return grb_1, grb_2, grb_3, grb_4, grb_5, grb_1_logic, grb_2_logic, grb_3_logic, grb_4_logic, grb_5_logic


def get_GRIB_file_values(GRIB_File):
 
    '''
    THIS FUNCTION RETURNS THE VALUES OF THE DATA INSIDE OF A GRIB FILE. 

    COPYRIGHT (C) ERIC J. DREWITZ 2023
    '''
    return GRIB_File.values


def get_GRIB_file_valid_date(GRIB_File):

    '''
    THIS FUNCTION RETURNS THE VALID DATE FOR A GRIB FILE

    COPYRIGHT (C) ERIC J. DREWITZ 2023
    '''
    return GRIB_File.validDate


    
        

    
