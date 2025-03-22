"""
This file is written by:

(C) Eric J. Drewitz 2025
        USDA/USFS

"""

import os
import matplotlib.pyplot as plt
import time
from zipfile import ZipFile
from PIL import Image
from datetime import datetime

class file_functions:

    '''
    This class hosts functions that build the file directory and/or file directory branches. 

    '''

    def forecast_cross_sections_graphics_paths(model, style, parameter, reference_system, start_coords=None, end_coords=None):

        r'''
        This function builds the directory for cross section graphics if the directory doesn't already exist. 

        Required Inputs:

        1) model (String) - The computer model used. 

        2) style (String) - The type of cross section (Time Cross-section vs. Cross-section between two points)

        3) parameter (String) - The parameter the user is analyzing

        4) reference_system (String) - The type of reference system used (i.e. States & Counties). 

        Optional Arguments:

        ** FOR CROSS-SECTION BETWEEN TWO POINTS ONLY **

        1) start_coords (tuple) - The starting latitude and longitude. 

        2) end_coords (tuple) - The ending latitude and longitude

        Returns: The path that is the branch for the specific cross-section graphics to the Weather Data directory. 

        '''


        if os.path.exists(f"Weather Data"):
            pass
        else:
            print(f"Built f:Weather Data")
            os.mkdir(f"Weather Data")

        if os.path.exists(f"Weather Data/Forecast Model Data"):
            pass

        else:
            os.mkdir(f"Weather Data/Forecast Model Data")
            print(f"Built f:Weather Data/Forecast Model Data Branch")

        if os.path.exists(f"Weather Data/Forecast Model Data/{model}"):
            pass

        else:
            os.mkdir(f"Weather Data/Forecast Model Data/{model}")
            print(f"Built f:Weather Data/Forecast Model Data/{model} Branch")

        if os.path.exists(f"Weather Data/Forecast Model Data/{model}/Cross Sections"):
            pass

        else:
            os.mkdir(f"Weather Data/Forecast Model Data/{model}/Cross Sections")
            print(f"Built f:Weather Data/Forecast Model Data/{model}/Cross Sections Branch")

        if os.path.exists(f"Weather Data/Forecast Model Data/{model}/Cross Sections/{style}"):
            pass

        else:
            os.mkdir(f"Weather Data/Forecast Model Data/{model}/Cross Sections/{style}")
            print(f"Built f:Weather Data/Forecast Model Data/{model}/Cross Sections/{style} Branch") 

        if os.path.exists(f"Weather Data/Forecast Model Data/{model}/Cross Sections/{style}/{reference_system}"):
            pass

        else:
            os.mkdir(f"Weather Data/Forecast Model Data/{model}/Cross Sections/{style}/{reference_system}")
            print(f"Built f:Weather Data/Forecast Model Data/{model}/Cross Sections/{style}/{reference_system} Branch") 

        if os.path.exists(f"Weather Data/Forecast Model Data/{model}/Cross Sections/{style}/{reference_system}/{parameter}"):
            pass

        else:
            os.mkdir(f"Weather Data/Forecast Model Data/{model}/Cross Sections/{style}/{reference_system}/{parameter}")
            print(f"Built f:Weather Data/Forecast Model Data/{model}/Cross Sections/{style}/{reference_system}/{parameter} Branch") 

        if start_coords != None and end_coords != None:
            start_lon = start_coords[1]
            start_lat = start_coords[0]
            end_lon = end_coords[1]
            end_lat = end_coords[0]

            slon = str(start_lon)
            slat = str(start_lat)
            elon = str(end_lon)
            elat = str(end_lat)

            if os.path.exists(f"Weather Data/Forecast Model Data/{model}/Cross Sections/{style}/{reference_system}/{parameter}/{slat}_{slon}_to_{elat}_{elon}"):
                pass
            else:
                os.mkdir(f"Weather Data/Forecast Model Data/{model}/Cross Sections/{style}/{reference_system}/{parameter}/{slat}_{slon}_to_{elat}_{elon}")
                print(f"Built f:Weather Data/Forecast Model Data/{model}/Cross Sections/{style}/{reference_system}/{parameter}/{slat}_{slon}_to_{elat}_{elon} Branch") 

            path = f"Weather Data/Forecast Model Data/{model}/Cross Sections/{style}/{reference_system}/{parameter}/{slat}_{slon}_to_{elat}_{elon}"
            path_print = f"f:Weather Data/Forecast Model Data/{model}/Cross Sections/{style}/{reference_system}/{parameter}/{slat}_{slon}_to_{elat}_{elon}"

        else:

            path = f"Weather Data/Forecast Model Data/{model}/Cross Sections/{style}/{reference_system}/{parameter}"
            path_print = f"f:Weather Data/Forecast Model Data/{model}/Cross Sections/{style}/{reference_system}/{parameter}"

        return path, path_print


    def point_forecast_sounding_graphics_paths(model, latitude, longitude, reference_system):

        r'''
        This function builds the paths in the directory for various forecast sounding graphics. 

        Required Arguments:

        1) model (String) - The computer model that is being used. 

        2) latitude (Integer or Float) - The latitude value in decimal degrees.

        3) longitude (Integer or Float) - The longitude value in decimal degrees. 

        4) reference_system (String) - The type of reference system used (i.e. States & Counties). 

        Returns: The path that is the branch for the forecast sounding graphics to the Weather Data directory. 

        '''

        if latitude >= 0:
            lat_symbol = 'N'
        if latitude < 0:
            latitude = latitude * -1
            lat_symbol = 'S'
        if longitude >= 0:
            lon_symbol = 'E'
        if longitude < 0:
            longitude = longitude * -1
            lon_symbol = 'W'

        if os.path.exists(f"Weather Data"):
            pass
        else:
            print(f"Weather Data Directory does not exist. Building Directory...")
            os.mkdir(f"Weather Data")

        if os.path.exists(f"Weather Data/Forecast Model Data"):
            pass

        else:
            os.mkdir(f"Weather Data/Forecast Model Data")
            print(f"Built f:Weather Data/Forecast Model Data Branch")

        if os.path.exists(f"Weather Data/Forecast Model Data/{model}"):
            pass

        else:
            os.mkdir(f"Weather Data/Forecast Model Data/{model}")
            print(f"Built f:Weather Data/Forecast Model Data/{model} Branch")

        if os.path.exists(f"Weather Data/Forecast Model Data/{model}/Soundings"):
            pass

        else:
            os.mkdir(f"Weather Data/Forecast Model Data/{model}/Soundings")
            print(f"Built f:Weather Data/Forecast Model Data/{model}/Soundings Branch")

        if os.path.exists(f"Weather Data/Forecast Model Data/{model}/Soundings/{str(round(float(latitude), 1))}{lat_symbol}"):
            pass

        else:
            os.mkdir(f"Weather Data/Forecast Model Data/{model}/Soundings/{str(round(float(latitude), 1))}{lat_symbol}")
            print(f"Built f:Weather Data/Forecast Model Data/{model}/Soundings/{str(round(float(latitude), 1))}{lat_symbol} Branch")
    
        if os.path.exists(f"Weather Data/Forecast Model Data/{model}/Soundings/{str(round(float(latitude), 1))}{lat_symbol}/{str(round(float(longitude), 1))}{lon_symbol}"):
            pass

        else:
            os.mkdir(f"Weather Data/Forecast Model Data/{model}/Soundings/{str(round(float(latitude), 1))}{lat_symbol}/{str(round(float(longitude), 1))}{lon_symbol}")
            print(f"Built f:Weather Data/Forecast Model Data/{model}/Soundings/{str(round(float(latitude), 1))}{lat_symbol}/{str(round(float(longitude), 1))}{lon_symbol} Branch")

        if os.path.exists(f"Weather Data/Forecast Model Data/{model}/Soundings/{str(round(float(latitude), 1))}{lat_symbol}/{str(round(float(longitude), 1))}{lon_symbol}/{reference_system}"):
            pass

        else:
            os.mkdir(f"Weather Data/Forecast Model Data/{model}/Soundings/{str(round(float(latitude), 1))}{lat_symbol}/{str(round(float(longitude), 1))}{lon_symbol}/{reference_system}")
            print(f"Built f:Weather Data/Forecast Model Data/{model}/Soundings/{str(round(float(latitude), 1))}{lat_symbol}/{str(round(float(longitude), 1))}{lon_symbol}/{reference_system} Branch")

        path = f"Weather Data/Forecast Model Data/{model}/Soundings/{str(round(float(latitude), 1))}{lat_symbol}/{str(round(float(longitude), 1))}{lon_symbol}/{reference_system}"
        path_print = f"f:Weather Data/Forecast Model Data/{model}/Soundings/{str(round(float(latitude), 1))}{lat_symbol}/{str(round(float(longitude), 1))}{lon_symbol}/{reference_system}"

        return path, path_print, lat_symbol, lon_symbol
        
    

    def forecast_model_graphics_paths(model, region, reference_system, parameter, str_level):

        r'''
        This function builds the paths in the directory for various forecast model graphics. 

        Required Arguments:

        1) model (String) - The computer model that is being used. 

        2) region (String) - The region abbreviation. 

        3) reference_system (String) - The type of reference system used (i.e. States & Counties). 

        4) parameter (String) - The parameter being analyzed. 

        5) str_level (String) - The value of the pressure level as a string. 

        Optional Arguments: None

        Returns: The path that is the branch for the forecast model graphics to the Weather Data directory. 

        '''

        model = model.upper()
        region = region.upper()
        parameter = parameter.upper()
        reference_system = reference_system.upper()
        str_level = str_level.upper()

        if os.path.exists(f"Weather Data"):
            pass
        else:
            print(f"Weather Data Directory does not exist. Building Directory...")
            os.mkdir(f"Weather Data")
            print(f"Successfully built f:Weather Data Directory.")

        if os.path.exists(f"Weather Data/Forecast Model Data"):
            pass

            if os.path.exists(f"Weather Data/Forecast Model Data/{model}"):
                pass

                if os.path.exists(f"Weather Data/Forecast Model Data/{model}/{region}"):
                    pass

                    if os.path.exists(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}"):
                        pass

                        if os.path.exists(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}"):
                            pass 

                            if os.path.exists(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level}"):
                                pass

                            else:
                                print(f"f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level} Directory does not exists.\nBuilding new branch automatically...") 
                                os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level}")
                                print(f"Successfully built f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level} Directory.")

                        else:
                            print(f"f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter} Directory does not exists.\nBuilding new branch automatically...") 
                            os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}")
                            print(f"Successfully built f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter} Directory.")
                            print(f"f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level} Directory does not exists.\nBuilding new branch automatically...") 
                            os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level}")
                            print(f"Successfully built f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level} Directory.")

                    else:
                        print(f"f:Forecast Model Data/{model}/{region}/{reference_system} Directory does not exists.\nBuilding new branch automatically...") 
                        os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}")
                        print(f"Successfully built f:Forecast Model Data/{model}/{region}/{reference_system} Directory.")
                        print(f"f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter} Directory does not exists.\nBuilding new branch automatically...") 
                        os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}")
                        print(f"Successfully built f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter} Directory.")

                        print(f"f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level} Directory does not exists.\nBuilding new branch automatically...") 
                        os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level}")
                        print(f"Successfully built f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level} Directory.")

                else:
                    print(f"f:Forecast Model Data/{model}/{region} Directory does not exists.\nBuilding new branches automatically...") 
                    os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}")
                    print(f"Successfully built f:Forecast Model Data/{model}/{region} Branch.")
                    os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}")
                    print(f"Successfully built f:Forecast Model Data/{model}/{region}/{reference_system} Directory.")
                    print(f"f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter} Directory does not exists.\nBuilding new branch automatically...") 
                    os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}")
                    print(f"Successfully built f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter} Directory.")

                    print(f"f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level} Directory does not exists.\nBuilding new branch automatically...") 
                    os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level}")
                    print(f"Successfully built f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level} Directory.")

            else:
                print(f"f:Forecast Model Data/{model} Directory does not exists.\nBuilding new branches automatically...") 
                os.mkdir(f"Weather Data/Forecast Model Data/{model}")
                print(f"Successfully built f:Forecast Model Data/{model} Branch.")
                os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}")
                print(f"Successfully built f:Forecast Model Data/{model}/{region} Branch.")
                os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}")
                print(f"Successfully built f:Forecast Model Data/{model}/{region}/{reference_system} Directory.")
                print(f"f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter} Directory does not exists.\nBuilding new branch automatically...") 
                os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}")
                print(f"Successfully built f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter} Directory.")

                print(f"f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level} Directory does not exists.\nBuilding new branch automatically...") 
                os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level}")
                print(f"Successfully built f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level} Directory.")

        else:
            print(f"f:Forecast Model Data Directory does not exists.\nBuilding new branches automatically...")
            os.mkdir(f"Weather Data/Forecast Model Data")
            print(f"Successfully built f:Forecast Model Data Branch.")
            os.mkdir(f"Weather Data/Forecast Model Data/{model}")
            print(f"Successfully built f:Forecast Model Data/{model} Branch.")
            os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}")
            print(f"Successfully built f:Forecast Model Data/{model}/{region} Branch.")
            os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}")
            print(f"Successfully built f:Forecast Model Data/{model}/{region}/{reference_system} Directory.")
            print(f"f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter} Directory does not exists.\nBuilding new branch automatically...") 
            os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}")
            print(f"Successfully built f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter} Directory.")

            print(f"f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level} Directory does not exists.\nBuilding new branch automatically...") 
            os.mkdir(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level}")
            print(f"Successfully built f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level} Directory.")

        path = f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level}"
        path_print = f"f:Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level}"
    
        return path, path_print


    def extract_zipped_files(file_path, extraction_folder):

        r'''
        This function unzips a file in a folder. 

        Required Arguments:

        1) file_path (String) - The path to the file that needs unzipping.

        2) extraction_folder (String) - The folder that the zipped files are located in.

        '''
    
        # Load the zipfile
        with ZipFile(file_path, 'r') as zObject:
            # extract a specific file in the zipped folder
            zObject.extractall(extraction_folder)
        zObject.close()

    def save_daily_sounding_graphic(figure, station_id, date):

        r'''
        This function builds the path for the observed sounding graphics and saves the file. 

        Required Arguments:

        1) figure (matplotlib figure) - The figure that needs to be saved. 

        2) station_id (String) - The station ID for the upper-air station. 

        3) date (datetime) - The date and time of the sounding. 

        '''

        station_id = station_id
        station_id = station_id.upper()
        fig = figure
        date = date

        if date == None:

            if os.path.exists(f"Weather Data"):
                pass
                if os.path.exists(f"Weather Data/Soundings"):
                    path = f"Weather Data/Soundings/{station_id}.png"
                    fig.savefig(path, bbox_inches='tight')
                    print(station_id+" Sounding Saved to "+path)
                else:
                    print("f:Weather Data/Soundings does not exist.\nBuilding Soundings branch...")
                    os.mkdir(f"Weather Data/Soundings")
                    print("Successfully built new branch to directory!")
                    path = f"Weather Data/Soundings/{station_id}.png"
                    fig.savefig(path, bbox_inches='tight')
                    print(station_id+" Sounding Saved to "+path)
            else:
                print("Setting up the Soundings folder and the rest of the file structure...")
                os.mkdir("Weather Data")        
                os.mkdir(f"Weather Data/Soundings")
                path = f"Weather Data/Soundings/{station_id}.png"
                fig.savefig(path, bbox_inches='tight')
                print(station_id+" Sounding Saved to "+path)

        else:
            
            date = date.strftime('%Y %m %d %H UTC')
            
            if os.path.exists(f"Weather Data"):
                pass
                if os.path.exists(f"Weather Data/Custom Date Soundings"):
                    pass
                    path = f"Weather Data/Custom Date Soundings/{station_id}_{date}.png"
                    fig.savefig(path, bbox_inches='tight')
                    print(station_id+" Sounding Saved to "+path)
                else:
                    print("f:Weather Data/Custom Soundings does not exist.\nBuilding Soundings branch...")
                    os.mkdir(f"Weather Data/Custom Date Soundings")
                    print("Successfully built new branch to directory!")
                    path = f"Weather Data/Custom Date Soundings/{station_id}_{date}.png"
                    fig.savefig(path, bbox_inches='tight')
                    print(station_id+" Sounding Saved to "+path)
            else:
                print("Setting up the Soundings folder and the rest of the file structure...")
                os.mkdir("Weather Data")        
                os.mkdir(f"Weather Data/Custom Date Soundings")
                path = f"Weather Data/Custom Date Soundings/{station_id}_{date}.png"
                fig.savefig(path, bbox_inches='tight')
                print(station_id+" Sounding Saved to "+path)            
    

    def save_daily_weather_summary(figure, station_id):

        r'''
        This function saves the daily weather summary to a path created by this function. 

        Required Arguments:

        1) figure (matplotlib figure) - The figure that needs to be saved. 

        2) station_id (String) - The station ID for the observation site. 

        '''

        station_id = station_id
        station_id = station_id.upper()
        fig = figure

        if os.path.exists(f"Weather Data"):
            pass
            if os.path.exists(f"Weather Data/Daily Weather Summary"):
                pass
                path = f"Weather Data/Daily Weather Summary/{station_id}.png"
                fig.savefig(path, bbox_inches='tight')
                print(station_id+" Daily Weather Summary Saved to "+path)
            else:
                print("f:Weather Data/Daily Weather Summary does not exist.\nBuilding Daily Weather Summary branch...")
                os.mkdir(f"Weather Data/Daily Weather Summary")
                print("Successfully built new branch to directory!")
                path = f"Weather Data/Daily Weather Summary/{station_id}.png"
                fig.savefig(path, bbox_inches='tight')
                print(station_id+" Daily Weather Summary Saved to "+path)
        else:
            print("Setting up the Weather Data folder and the rest of the file structure...")
            os.mkdir("Weather Data")        
            os.mkdir(f"Weather Data/Daily Weather Summary")
            os.mkdir(f"Weather Data/Daily Weather Summary")
            path = f"Weather Data/Daily Weather Summary/{station_id}.png"
            fig.savefig(path, bbox_inches='tight')
            print(station_id+" Daily Weather Summary Saved to "+path)


    def noaa_graphics_paths(state, gacc_region, plot_type, reference_system, cwa, spc=False):

        r'''
        This function creates the file directory for the images to save to. 

        Required Arguments:

        1) state (String) - The two letter state abbreviation in both upper or lower case
        2) gacc_region (String) - The 4-letter GACC Region abbreviation
        3) plot_type (String) - The type of product to be plotted (i.e. Maximum Temperature Forecast)
        4) reference_system (String) - The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
            2) 'States Only'
            3) 'GACC Only'
            4) 'GACC & PSA'
            5) 'CWA Only'
            6) 'NWS CWAs & NWS Public Zones'
            7) 'NWS CWAs & NWS Fire Weather Zones'
            8) 'NWS CWAs & Counties'
            9) 'GACC & PSA & NWS Fire Weather Zones'
            10) 'GACC & PSA & NWS Public Zones'
            11) 'GACC & PSA & NWS CWA'
            12) 'GACC & PSA & Counties'
            13) 'GACC & Counties'

        5) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            2) ALU - NWS Anchorage West Domain
            3) AJK - NWS Juneau
            4) AFG - NWS Fairbanks

        Optional Arguments:

        1) spc (Boolean) - Default = False. - If set to True, the graphics will be saved to the SPC Outlooks branch.
           If set to fale, the graphics will be saved to the NWS Forecasts branch. 

        Return: The file path of the directory branch
        '''

        if state == None and gacc_region != None:
            state = gacc_region

        else:
            state = state

        plot_type = plot_type
        cwa = cwa
        state = state.upper()
        plot_type = plot_type.upper()
        try:
            cwa = cwa.upper()
        except Exception as e:
            pass

        if spc == True:
            folder = "SPC Outlooks"
        else:
            folder = "NWS Forecasts"

        if os.path.exists(f"Weather Data"):
            pass
        else:
            os.mkdir(f"Weather Data")
            print(f"Built f:Weather Data")

        if os.path.exists(f"Weather Data/{folder}"):
            pass
        else:
            os.mkdir(f"Weather Data/{folder}")
            print(f"Built f:Weather Data/{folder}")

        if os.path.exists(f"Weather Data/{folder}/{plot_type}"):
            pass
        else:
            os.mkdir(f"Weather Data/{folder}/{plot_type}")
            print(f"Built f:Weather Data/{folder}/{plot_type}")

        if os.path.exists(f"Weather Data/{folder}/{plot_type}/{state}"):
            pass
        else:
            os.mkdir(f"Weather Data/{folder}/{plot_type}/{state}")
            print(f" Built f:Weather Data/{folder}/{plot_type}/{state}")

        if os.path.exists(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}"):
            pass
        else:
            os.mkdir(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}")
            print(f"Built f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}")


        if state == 'AK' or state == 'ak':

            if cwa == None:
                cwa = 'STATE'
            else:
                cwa = cwa

            if os.path.exists(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}"):
                pass
            else:
                os.mkdir(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}")
                print(f"Built f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}")                
        
            path = f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}"
            path_print = f"f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}"

        
        else:
            path = f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}"
            path_print = f"f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}"

        return path, path_print

    def rtma_graphics_paths(state, gacc_region, plot_type, reference_system, cwa):

        r'''
        This function creates the file directory for the images to save to. 

        Required Arguments:

        1) state (String) - The two letter state abbreviation in both upper or lower case
        2) gacc_region (String) - The 4-letter GACC Region abbreviation
        3) plot_type (String) - The type of product to be plotted (i.e. Maximum Temperature Forecast)
        4) reference_system (String) - The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
            2) 'States Only'
            3) 'GACC Only'
            4) 'GACC & PSA'
            5) 'CWA Only'
            6) 'NWS CWAs & NWS Public Zones'
            7) 'NWS CWAs & NWS Fire Weather Zones'
            8) 'NWS CWAs & Counties'
            9) 'GACC & PSA & NWS Fire Weather Zones'
            10) 'GACC & PSA & NWS Public Zones'
            11) 'GACC & PSA & NWS CWA'
            12) 'GACC & PSA & Counties'
            13) 'GACC & Counties'

        5) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            2) ALU - NWS Anchorage West Domain
            3) AJK - NWS Juneau
            4) AFG - NWS Fairbanks

        Optional Arguments:
        
        1) spc (Boolean) - Default = False. - If set to True, the graphics will be saved to the SPC Outlooks branch.
           If set to fale, the graphics will be saved to the NWS Forecasts branch. 

        Return: The file path of the directory branch
        '''

        if state == None and gacc_region != None:
            state = gacc_region

        else:
            state = state

        plot_type = plot_type
        cwa = cwa
        state = state.upper()
        plot_type = plot_type.upper()
        try:
            cwa = cwa.upper()
        except Exception as e:
            pass

        folder = 'RTMA'

        if os.path.exists(f"Weather Data"):
            pass
        else:
            os.mkdir(f"Weather Data")
            print(f"Built f:Weather Data")

        if os.path.exists(f"Weather Data/{folder}"):
            pass
        else:
            os.mkdir(f"Weather Data/{folder}")
            print(f"Built f:Weather Data/{folder}")

        if os.path.exists(f"Weather Data/{folder}/{plot_type}"):
            pass
        else:
            os.mkdir(f"Weather Data/{folder}/{plot_type}")
            print(f"Built f:Weather Data/{folder}/{plot_type}")

        if os.path.exists(f"Weather Data/{folder}/{plot_type}/{state}"):
            pass
        else:
            os.mkdir(f"Weather Data/{folder}/{plot_type}/{state}")
            print(f" Built f:Weather Data/{folder}/{plot_type}/{state}")

        if os.path.exists(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}"):
            pass
        else:
            os.mkdir(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}")
            print(f"Built f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}")


        if state == 'AK' or state == 'ak':

            if cwa == None:
                cwa = 'STATE'
            else:
                cwa = cwa

            if os.path.exists(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}"):
                pass
            else:
                os.mkdir(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}")
                print(f"Built f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}")                
        
            path = f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}"
            path_print = f"f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}"

        
        else:
            path = f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}"
            path_print = f"f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}"

        return path, path_print


    def obs_graphics_paths(state, gacc_region, plot_type, reference_system, cwa, interp=False, interp_type=None):

        r'''
        This function creates the file directory for the images to save to. 

        Required Arguments:

        1) state (String) - The two letter state abbreviation in both upper or lower case
        2) gacc_region (String) - The 4-letter GACC Region abbreviation
        3) plot_type (String) - The type of product to be plotted (i.e. Maximum Temperature Forecast)
        4) reference_system (String) - The georgraphical reference system with respect to the borders on the map. If the user
            wishes to use a reference system not on this list, please see items 17-23. 
            Reference Systems: 
            
            1) 'States & Counties'
            2) 'States Only'
            3) 'GACC Only'
            4) 'GACC & PSA'
            5) 'CWA Only'
            6) 'NWS CWAs & NWS Public Zones'
            7) 'NWS CWAs & NWS Fire Weather Zones'
            8) 'NWS CWAs & Counties'
            9) 'GACC & PSA & NWS Fire Weather Zones'
            10) 'GACC & PSA & NWS Public Zones'
            11) 'GACC & PSA & NWS CWA'
            12) 'GACC & PSA & Counties'
            13) 'GACC & Counties'

        5) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA

            NWS CWA Abbreviations:
    
            1) AER - NWS Anchorage East Domain
            2) ALU - NWS Anchorage West Domain
            3) AJK - NWS Juneau
            4) AFG - NWS Fairbanks

        Optional Arguments:

        1) interp (Boolean) - Default=False. This is only set to True for graphics requiring interpolation methods (Gridded Observations). 

        2) interp_type (String) - The type of interpolation method used. interp=True must be set for this to be used. 

        Return: The file path of the directory branch for observations graphics. 
        '''

        if state == None and gacc_region != None:
            state = gacc_region

        else:
            state = state

        plot_type = plot_type
        cwa = cwa
        state = state.upper()
        plot_type = plot_type.upper()
        try:
            cwa = cwa.upper()
        except Exception as e:
            pass

        folder = 'Observations'

        if os.path.exists(f"Weather Data"):
            pass
        else:
            os.mkdir(f"Weather Data")
            print(f"Built f:Weather Data")

        if os.path.exists(f"Weather Data/{folder}"):
            pass
        else:
            os.mkdir(f"Weather Data/{folder}")
            print(f"Built f:Weather Data/{folder}")

        if os.path.exists(f"Weather Data/{folder}/{plot_type}"):
            pass
        else:
            os.mkdir(f"Weather Data/{folder}/{plot_type}")
            print(f"Built f:Weather Data/{folder}/{plot_type}")

        if os.path.exists(f"Weather Data/{folder}/{plot_type}/{state}"):
            pass
        else:
            os.mkdir(f"Weather Data/{folder}/{plot_type}/{state}")
            print(f" Built f:Weather Data/{folder}/{plot_type}/{state}")

        if os.path.exists(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}"):
            pass
        else:
            os.mkdir(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}")
            print(f"Built f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}")

        if interp != None and state != 'AK' and state != 'ak':
            if os.path.exists(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{interp_type}"):
                pass
            else:
                os.mkdir(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{interp_type}")
                print(f"Built f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{interp_type}")            

        if state == 'AK' or state == 'ak':

            cwa = cwa
            if cwa == None:
                cwa = 'STATE'
            else:
                cwa = cwa

            if os.path.exists(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}"):
                pass
            else:
                os.mkdir(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}")
                print(f"Built f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}")                

            if interp != None:
                if os.path.exists(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}/{interp_type}"):
                    pass
                else:
                    os.mkdir(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}/{interp_type}")
                    print(f"Built f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}/{interp_type}")  

                path = f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}/{interp_type}"
                path_print = f"f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}/{interp_type}"
            else:
                path = f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}"
                path_print = f"f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}"
        
        else:
            if interp == None:
                path = f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}"
                path_print = f"f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}"
            else:
                path = f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{interp_type}"
                path_print = f"f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{interp_type}"                

        return path, path_print
