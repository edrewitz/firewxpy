

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
    
        # Load the zipfile
        with ZipFile(file_path, 'r') as zObject:
            # extract a specific file in the zipped folder
            zObject.extractall(extraction_folder)
        zObject.close()

    def save_daily_sounding_graphic(figure, station_id, date):

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


    def noaa_graphics_paths(state, gacc_region, plot_type, reference_system, cwa, island=None, spc=False):

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

        Optional Arguments:

        1) island (String) - *For Hawaii only* - The name of the island
        2) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA
        3) spc (Boolean) - Default = False. - If set to True, the graphics will be saved to the SPC Outlooks branch.
           If set to fale, the graphics will be saved to the NWS Forecasts branch. 

        NWS CWA Abbreviations:

        1) AER - NWS Anchorage East Domain
        2) ALU - NWS Anchorage West Domain
        3) AJK - NWS Juneau
        4) AFG - NWS Fairbanks

        Return: The file path of the directory branch
        '''

        if state == None and gacc_region != None:
            state = gacc_region

        else:
            state = state

        plot_type = plot_type
        island = island
        cwa = cwa
        state = state.upper()
        plot_type = plot_type.upper()
        try:
            island = island.upper()
        except Exception as e:
            pass
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

        if state == 'HI' or state == 'hi':
            island = island
            
            if os.path.exists(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{island}"):
                pass
            else:
                os.mkdir(f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{island}")
                print(f"Built f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{island}")

            path = f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{island}"
            path_print = f"f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{island}"
         
        
            path = f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{island}"
            path_print = f"f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{island}"


        elif state == 'AK' or state == 'ak':

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


    def obs_graphics_paths(state, gacc_region, plot_type, reference_system, cwa):

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

        Optional Arguments:

        1) island (String) - *For Hawaii only* - The name of the island
        2) cwa (String) - *For Alaska only* - The 3-letter abbreviation for the National Weather Service CWA
        3) spc (Boolean) - Default = False. - If set to True, the graphics will be saved to the SPC Outlooks branch.
           If set to fale, the graphics will be saved to the NWS Forecasts branch. 

        NWS CWA Abbreviations:

        1) AER - NWS Anchorage East Domain
        2) ALU - NWS Anchorage West Domain
        3) AJK - NWS Juneau
        4) AFG - NWS Fairbanks

        Return: The file path of the directory branch
        '''

        if state == None and gacc_region != None:
            state = gacc_region

        else:
            state = state

        plot_type = plot_type
        island = island
        cwa = cwa
        state = state.upper()
        plot_type = plot_type.upper()
        try:
            island = island.upper()
        except Exception as e:
            pass
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
        
            path = f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}"
            path_print = f"f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}/{cwa}"

        
        else:
            path = f"Weather Data/{folder}/{plot_type}/{state}/{reference_system}"
            path_print = f"f:Weather Data/{folder}/{plot_type}/{state}/{reference_system}"

        return path, path_print
