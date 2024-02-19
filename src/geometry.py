'''
This file consists of functions that read in the shapefiles for both the Geographic Area Coordination Center (GACC) Boundaries and Predictive Services Areas (PSA) boundaries. 
These files can be downloaded from either the FireWxPy Github or on NIFC's website. 

This file was written by Meteorologist Eric J. Drewitz 

            (C) Meteorologist Eric J. Drewitz 
                        USDA/USFS

'''
###### IMPORTS ################
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature


class info:

    '''
    This class hosts all the error messages that will be returned to the user. 

    '''

    def PSA_shape_file_error():

        '''
        This function returns an error message for the user if the shapefile is not found. 
        '''
        error_msg = f"""
        
        WARNING: COULD NOT FIND FILE. PLEASE MAKE SURE YOU HAVE THE CORRECT FILE PATH. 

        ALSO, BE SURE TO HAVE ALL THE FILES AS FOLLOWS LOCATED IN THE SAME PLACE.
        THE FILES NEEDED IN THE SAME PLACE ARE NAMED AS FOLLOWS:

        National_PSA_Current.shp
        National_PSA_Current.shx
        National_PSA_Current.xml
        National_PSA_Current.cpg
        National_PSA_Current.dbf
        National_PSA_Current.prj

        WHEN DOWNLOADING THESE SHAPEFILES FROM NIFC'S WEBSITE: https://data-nifc.opendata.arcgis.com/datasets/e580f3fd4d644366b121676714d69c2d/explore

        THE XML FILE BY DEFAULT HAS A DIFFERENT NAME THAN THE REST. RENAME THE XML FILE TO MATCH ALL OF THE OTHERFILE NAMES

        THE FILE NAMES SHOULD BE CALLED: "National_PSA_Current".FILETYPE

        """
        return error_msg


class Predictive_Services_Areas:

    '''
    This class hosts the functions that return the GACC and PSA Boundaries

    '''

    def get_PSAs(line_color):

        r'''
        This function reads the shapefile (.SHP) and returns the geometries for the PSA boundaries in the color specified by the user.

        This function is to only be used if the files are in the same folder the script is running. 

        '''

        fname = 'National_PSA_Current.shp'
        
        try:
            shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                           ccrs.PlateCarree(), facecolor=(0,0,0,0), edgecolor=line_color)
        
            return shape_feature

        except Exception as a:
            error = info.PSA_shape_file_error()
            print(error)


    def get_PSAs_custom_file_path(file_path, line_color):

        r'''
        This function reads the shapefile (.SHP) and returns the geometries for the PSA boundaries in the color specified by the user.

        This function is to be used if the user wishes to run the script in a seperate folder than the folder that hosts the shapefiles. 

        '''
        
        
        try:
            shape_feature = ShapelyFeature(Reader(file_path).geometries(),
                                           ccrs.PlateCarree(), facecolor=(0,0,0,0), edgecolor=line_color)
        
            return shape_feature

        except Exception as a:
            error = info.PSA_shape_file_error()
            print(error)


    def get_GACC_Boundaries(line_color):

        r'''
        This function reads the shapefile (.SHP) and returns the geometries for the GACC boundaries in the color specified by the user.

        This function is to only be used if the files are in the same folder the script is running. 

        '''

        fname = 'National_GACC_Current.shp'
        
        try:
            shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                           ccrs.PlateCarree(), facecolor=(0,0,0,0), edgecolor=line_color)
        
            return shape_feature

        except Exception as a:
            error = info.PSA_shape_file_error()
            print(error)

    
    def get_GACC_Boundaries_custom_file_path(file_path, line_color):

        r'''
        This function reads the shapefile (.SHP) and returns the geometries for the GACC boundaries in the color specified by the user.

        This function is to be used if the user wishes to run the script in a seperate folder than the folder that hosts the shapefiles. 

        '''
        
        
        try:
            shape_feature = ShapelyFeature(Reader(file_path).geometries(),
                                           ccrs.PlateCarree(), facecolor=(0,0,0,0), edgecolor=line_color)
        
            return shape_feature

        except Exception as a:
            error = info.PSA_shape_file_error()
            print(error)
