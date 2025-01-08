import os
import imageio
import matplotlib.pyplot as plt
import time
from zipfile import ZipFile
from PIL import Image
from datetime import datetime

class file_functions:

    def forecast_model_graphics_paths(model, region, reference_system, parameter, str_level):

        model = model.upper()
        region = region.upper()
        parameter = parameter.upper()
        reference_system = reference_system.upper()
        str_level = str_level.upper()

        if os.path.exists(f"Weather Data"):
            print(f"Already Satisfied: f:Weather Data Parent Directory exists.")
        else:
            print(f"Weather Data Directory does not exist. Building Directory...")
            os.mkdir(f"Weather Data")
            print(f"Successfully built f:Weather Data Directory.")

        if os.path.exists(f"Weather Data/Forecast Model Data"):
            print(f"Already Satisfied: f:Forecast Model Data Directory exists.") 

            if os.path.exists(f"Weather Data/Forecast Model Data/{model}"):
                print(f"Already Satisfied: f:Forecast Model Data/{model} Directory exists.") 

                if os.path.exists(f"Weather Data/Forecast Model Data/{model}/{region}"):
                    print(f"Already Satisfied: f:Forecast Model Data/{model}/{region} Directory exists.") 

                    if os.path.exists(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}"):
                        print(f"Already Satisfied: f:Forecast Model Data/{model}/{region}/{reference_system} Directory exists.") 

                        if os.path.exists(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}"):
                            print(f"Already Satisfied: f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter} Directory exists.")  

                            if os.path.exists(f"Weather Data/Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level}"):
                                print(f"Already Satisfied: f:Forecast Model Data/{model}/{region}/{reference_system}/{parameter}/{str_level} Directory exists.") 

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


    def update_images(figure_list, path, GIF_path, plot_type):

        
        plot_type = plot_type
        figure_list = figure_list
        path = path
        GIF_path = GIF_path

        if plot_type == 'RTMA LOW AND HIGH RH':
            
            fig = figure_list

            fig = fig.savefig(path+'/RTMA LOW AND HIGH RH.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA LOW AND HIGH RH.png")              

        if plot_type == 'RTMA WIND GUST & OBS':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA WIND GUST & OBS.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA WIND GUST & OBS.png")                

        if plot_type == 'RTMA WIND SPEED & OBS':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA WIND SPEED & OBS.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA WIND SPEED & OBS.png")             

        if plot_type == 'RTMA DEW POINT ADVECTION':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA DEW POINT ADVECTION.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA DEW POINT ADVECTION.png")              

        if plot_type == 'RTMA RH ADVECTION':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA RH ADVECTION.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA RH ADVECTION.png")  

        if plot_type == 'RTMA TEMPERATURE ADVECTION':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA TEMPERATURE ADVECTION.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA TEMPERATURE ADVECTION.png")  

        if plot_type == 'RTMA EXTREME HEAT':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA EXTREME HEAT.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA EXTREME HEAT.png")     

        if plot_type == 'RTMA FROST FREEZE':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA FROST FREEZE.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA FROST FREEZE.png")            

        if plot_type == 'RTMA LOW RH & METAR':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA LOW RH & METAR.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA LOW RH & METAR.png")

        if plot_type == 'RTMA RH & METAR':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA RH & METAR.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA RH & METAR.png")

        if plot_type == 'RTMA DRY & WINDY AREAS WIND VECTORS':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA DRY & WINDY AREAS WIND VECTORS.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA DRY & WINDY AREAS WIND VECTORS.png")

        if plot_type == 'RTMA DRY & WINDY AREAS WIND BARBS':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA DRY & WINDY AREAS WIND BARBS.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA DRY & WINDY AREAS WIND BARBS.png")

        if plot_type == 'RTMA DRY & WINDY AREAS SAMPLE POINTS':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA DRY & WINDY AREAS SAMPLE POINTS.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA DRY & WINDY AREAS SAMPLE POINTS.png")  

        if plot_type == 'RTMA DRY & GUSTY AREAS':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA DRY & GUSTY AREAS.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA DRY & GUSTY AREAS.png")    
           

        if plot_type == 'RTMA WIND SPEED & DIRECTION WIND VECTORS':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA WIND SPEED & DIRECTION WIND VECTORS.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA WIND SPEED & DIRECTION COMPARISON WIND VECTORS.png")  

        if plot_type == 'RTMA WIND SPEED & DIRECTION WIND BARBS':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA WIND SPEED & DIRECTION WIND BARBS.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA WIND SPEED & DIRECTION WIND BARBS.png")     

        if plot_type == '24HR RTMA WIND SPEED & DIRECTION COMPARISON WIND VECTORS':

            fig = figure_list

            fig = fig.savefig(path+'/24HR RTMA WIND SPEED & DIRECTION COMPARISON WIND VECTORS.png', bbox_inches='tight')

            print("Image saved to: "+path+"/24HR RTMA WIND SPEED & DIRECTION COMPARISON WIND VECTORS.png")              

        if plot_type == '24HR RTMA WIND SPEED & DIRECTION COMPARISON WIND BARBS':

            fig = figure_list

            fig = fig.savefig(path+'/24HR RTMA WIND SPEED & DIRECTION COMPARISON WIND BARBS.png', bbox_inches='tight')

            print("Image saved to: "+path+"/24HR RTMA WIND SPEED & DIRECTION COMPARISON WIND BARBS.png")             

        if plot_type == 'RTMA WIND SPEED':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA WIND SPEED.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA WIND SPEED.png")              

        if plot_type == '24HR RTMA WIND SPEED COMPARISON':
            
            fig = figure_list

            fig = fig.savefig(path+'/24HR RTMA WIND SPEED COMPARISON.png', bbox_inches='tight')

            print("Image saved to: "+path+"/24HR RTMA WIND SPEED COMPARISON.png")  
            
        if plot_type == '24HR RTMA DEW POINT COMPARISON':

            fig = figure_list

            fig = fig.savefig(path+'/24HR RTMA DEW POINT COMPARISON.png', bbox_inches='tight')

            print("Image saved to: "+path+"/24HR RTMA DEW POINT COMPARISON.png")              

        if plot_type == 'RTMA DEW POINT':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA DEW POINT.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA DEW POINT.png")  
            

        if plot_type == '24HR RTMA TOTAL CLOUD COVER COMPARISON':

            fig = figure_list

            fig = fig.savefig(path+'/24HR RTMA TOTAL CLOUD COVER COMPARISON.png', bbox_inches='tight')

            print("Image saved to: "+path+"/24HR RTMA TOTAL CLOUD COVER COMPARISON.png")           

        if plot_type == 'RTMA TOTAL CLOUD COVER':
            
            fig = figure_list

            fig = fig.savefig(path+'/RTMA TOTAL CLOUD COVER.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA TOTAL CLOUD COVER.png")

        if plot_type == '24HR RTMA TEMPERATURE COMPARISON':

            fig = figure_list

            fig = fig.savefig(path+'/24HR RTMA TEMPERATURE COMPARISON.png', bbox_inches='tight')

            print("Image saved to: "+path+"/24HR RTMA TEMPERATURE COMPARISON.png")

        if plot_type == 'RTMA TEMPERATURE':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA TEMPERATURE.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA TEMPERATURE.png")

        if plot_type == 'RTMA RH':

            fig = figure_list

            fig = fig.savefig(path+'/RTMA RH.png', bbox_inches='tight')

            print("Image saved to: "+path+"/RTMA RH.png")

        if plot_type == '24HR RTMA RH COMPARISON':

            fig = figure_list

            fig = fig.savefig(path+'/24HR RTMA RH COMPARISON.png', bbox_inches='tight')

            print("Image saved to: "+path+"/24HR RTMA RH COMPARISON.png")

        if plot_type == 'NWS Maximum RH Trend':

            file_path_1 = path+"/Night 2.png" 
            file_path_2 = path+"/Night 3.png" 
            file_path_3 = path+"/Night 4.png" 
            file_path_4 = path+"/Night 5.png" 
            file_path_5 = path+"/Night 6.png" 
            file_path_6 = path+"/Night 7.png" 

            GIF = GIF_path+"/NWS Maximum RH Trend.gif"

            try:
                os.remove(file_path_1)
                os.remove(file_path_2)
                os.remove(file_path_3)
                os.remove(file_path_4)
                os.remove(file_path_5)
                os.remove(file_path_6)
            except Exception as e:
                try:
                    os.remove(file_path_1)
                    os.remove(file_path_2)
                    os.remove(file_path_3)
                    os.remove(file_path_4)
                    os.remove(file_path_5)
                except Exception as e:
                    pass

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, None)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, None, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

        if plot_type == 'NWS Maximum RH':

            file_path_1 = path+"/Night 1.png" 
            file_path_2 = path+"/Night 2.png" 
            file_path_3 = path+"/Night 3.png" 
            file_path_4 = path+"/Night 4.png" 
            file_path_5 = path+"/Night 5.png" 
            file_path_6 = path+"/Night 6.png" 
            file_path_7 = path+"/Night 7.png" 

            GIF = GIF_path+"/NWS Maximum RH.gif"

            try:
                os.remove(file_path_1)
                os.remove(file_path_2)
                os.remove(file_path_3)
                os.remove(file_path_4)
                os.remove(file_path_5)
                os.remove(file_path_6)
                os.remove(file_path_7)
            except Exception as e:
                try:
                    os.remove(file_path_1)
                    os.remove(file_path_2)
                    os.remove(file_path_3)
                    os.remove(file_path_4)
                    os.remove(file_path_5)
                    os.remove(file_path_6)
                except Exception as e:
                    pass
                

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

        if plot_type == 'NWS Poor Overnight Recovery':

            file_path_1 = path+"/Night 1.png" 
            file_path_2 = path+"/Night 2.png" 
            file_path_3 = path+"/Night 3.png" 
            file_path_4 = path+"/Night 4.png" 
            file_path_5 = path+"/Night 5.png" 
            file_path_6 = path+"/Night 6.png" 
            file_path_7 = path+"/Night 7.png" 

            GIF = GIF_path+"/NWS Poor Overnight Recovery.gif"

            try:
                os.remove(file_path_1)
                os.remove(file_path_2)
                os.remove(file_path_3)
                os.remove(file_path_4)
                os.remove(file_path_5)
                os.remove(file_path_6)
                os.remove(file_path_7)
            except Exception as e:
                try:
                    os.remove(file_path_1)
                    os.remove(file_path_2)
                    os.remove(file_path_3)
                    os.remove(file_path_4)
                    os.remove(file_path_5)
                    os.remove(file_path_6)
                except Exception as e:
                    pass

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

        if plot_type == 'NWS Excellent Overnight Recovery':

            file_path_1 = path+"/Night 1.png" 
            file_path_2 = path+"/Night 2.png" 
            file_path_3 = path+"/Night 3.png" 
            file_path_4 = path+"/Night 4.png" 
            file_path_5 = path+"/Night 5.png" 
            file_path_6 = path+"/Night 6.png" 
            file_path_7 = path+"/Night 7.png" 

            GIF = GIF_path+"/NWS Excellent Overnight Recovery.gif"

            try:
                os.remove(file_path_1)
                os.remove(file_path_2)
                os.remove(file_path_3)
                os.remove(file_path_4)
                os.remove(file_path_5)
                os.remove(file_path_6)
                os.remove(file_path_7)
            except Exception as e:
                try:
                    os.remove(file_path_1)
                    os.remove(file_path_2)
                    os.remove(file_path_3)
                    os.remove(file_path_4)
                    os.remove(file_path_5)
                    os.remove(file_path_6)
                except Exception as e:
                    pass

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

        if plot_type == 'NWS Low Minimum RH':

            file_path_1 = path+"/Day 1.png" 
            file_path_2 = path+"/Day 2.png" 
            file_path_3 = path+"/Day 3.png" 
            file_path_4 = path+"/Day 4.png" 
            file_path_5 = path+"/Day 5.png" 
            file_path_6 = path+"/Day 6.png" 
            file_path_7 = path+"/Day 7.png" 

            GIF = GIF_path+"/NWS Low Minimum RH.gif"

            try:
                os.remove(file_path_1)
                os.remove(file_path_2)
                os.remove(file_path_3)
                os.remove(file_path_4)
                os.remove(file_path_5)
                os.remove(file_path_6)
                os.remove(file_path_7)
            except Exception as e:
                try:
                    os.remove(file_path_1)
                    os.remove(file_path_2)
                    os.remove(file_path_3)
                    os.remove(file_path_4)
                    os.remove(file_path_5)
                    os.remove(file_path_6)
                except Exception as e:
                    pass

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

        if plot_type == 'NWS Minimum RH':

            file_path_1 = path+"/Day 1.png" 
            file_path_2 = path+"/Day 2.png" 
            file_path_3 = path+"/Day 3.png" 
            file_path_4 = path+"/Day 4.png" 
            file_path_5 = path+"/Day 5.png" 
            file_path_6 = path+"/Day 6.png" 
            file_path_7 = path+"/Day 7.png" 

            GIF = GIF_path+"/NWS Minimum RH.gif"

            try:
                os.remove(file_path_1)
                os.remove(file_path_2)
                os.remove(file_path_3)
                os.remove(file_path_4)
                os.remove(file_path_5)
                os.remove(file_path_6)
                os.remove(file_path_7)
            except Exception as e:
                try:
                    os.remove(file_path_1)
                    os.remove(file_path_2)
                    os.remove(file_path_3)
                    os.remove(file_path_4)
                    os.remove(file_path_5)
                    os.remove(file_path_6)
                except Exception as e:
                    pass

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

        if plot_type == 'NWS Minimum RH Trend':

            file_path_1 = path+"/Day 2.png" 
            file_path_2 = path+"/Day 3.png" 
            file_path_3 = path+"/Day 4.png" 
            file_path_4 = path+"/Day 5.png" 
            file_path_5 = path+"/Day 6.png" 
            file_path_6 = path+"/Day 7.png" 

            GIF = GIF_path+"/NWS Minimum RH Trend.gif"

            try:
                os.remove(file_path_1)
                os.remove(file_path_2)
                os.remove(file_path_3)
                os.remove(file_path_4)
                os.remove(file_path_5)
                os.remove(file_path_6)
            except Exception as e:
                try:
                    os.remove(file_path_1)
                    os.remove(file_path_2)
                    os.remove(file_path_3)
                    os.remove(file_path_4)
                    os.remove(file_path_5)
                except Exception as e:
                    pass

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, None)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, None, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

        if plot_type == 'NWS Extreme Heat':

            file_path_1 = path+"/Day 1.png" 
            file_path_2 = path+"/Day 2.png" 
            file_path_3 = path+"/Day 3.png" 
            file_path_4 = path+"/Day 4.png" 
            file_path_5 = path+"/Day 5.png" 
            file_path_6 = path+"/Day 6.png" 
            file_path_7 = path+"/Day 7.png" 

            GIF = GIF_path+"/NWS Extreme Heat.gif"

            try:
                os.remove(file_path_1)
                os.remove(file_path_2)
                os.remove(file_path_3)
                os.remove(file_path_4)
                os.remove(file_path_5)
                os.remove(file_path_6)
                os.remove(file_path_7)
            except Exception as e:
                try:
                    os.remove(file_path_1)
                    os.remove(file_path_2)
                    os.remove(file_path_3)
                    os.remove(file_path_4)
                    os.remove(file_path_5)
                    os.remove(file_path_6)
                except Exception as e:
                    pass

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

        if plot_type == 'NWS Max T':

            file_path_1 = path+"/Day 1.png" 
            file_path_2 = path+"/Day 2.png" 
            file_path_3 = path+"/Day 3.png" 
            file_path_4 = path+"/Day 4.png" 
            file_path_5 = path+"/Day 5.png" 
            file_path_6 = path+"/Day 6.png" 
            file_path_7 = path+"/Day 7.png" 

            GIF = GIF_path+"/NWS Max T.gif"

            try:
                os.remove(file_path_1)
                os.remove(file_path_2)
                os.remove(file_path_3)
                os.remove(file_path_4)
                os.remove(file_path_5)
                os.remove(file_path_6)
                os.remove(file_path_7)
            except Exception as e:
                try:
                    os.remove(file_path_1)
                    os.remove(file_path_2)
                    os.remove(file_path_3)
                    os.remove(file_path_4)
                    os.remove(file_path_5)
                    os.remove(file_path_6)
                except Exception as e:
                    pass

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

        if plot_type == 'NWS Max T Trend':

            file_path_1 = path+"/Day 2.png" 
            file_path_2 = path+"/Day 3.png" 
            file_path_3 = path+"/Day 4.png" 
            file_path_4 = path+"/Day 5.png" 
            file_path_5 = path+"/Day 6.png" 
            file_path_6 = path+"/Day 7.png" 

            GIF = GIF_path+"/NWS Max T Trend.gif"

            try:
                os.remove(file_path_1)
                os.remove(file_path_2)
                os.remove(file_path_3)
                os.remove(file_path_4)
                os.remove(file_path_5)
                os.remove(file_path_6)
            except Exception as e:
                try:
                    os.remove(file_path_1)
                    os.remove(file_path_2)
                    os.remove(file_path_3)
                    os.remove(file_path_4)
                    os.remove(file_path_5)
                except Exception as e:
                    pass

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, None)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, None, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

        if plot_type == 'NWS Warm Min T':

            file_path_1 = path+"/Night 1.png" 
            file_path_2 = path+"/Night 2.png" 
            file_path_3 = path+"/Night 3.png" 
            file_path_4 = path+"/Night 4.png" 
            file_path_5 = path+"/Night 5.png" 
            file_path_6 = path+"/Night 6.png" 
            file_path_7 = path+"/Night 7.png" 

            GIF = GIF_path+"/NWS Warm Min T.gif"

            try:
                os.remove(file_path_1)
                os.remove(file_path_2)
                os.remove(file_path_3)
                os.remove(file_path_4)
                os.remove(file_path_5)
                os.remove(file_path_6)
                os.remove(file_path_7)
            except Exception as e:
                try:
                    os.remove(file_path_1)
                    os.remove(file_path_2)
                    os.remove(file_path_3)
                    os.remove(file_path_4)
                    os.remove(file_path_5)
                    os.remove(file_path_6)
                except Exception as e:
                    pass

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

        if plot_type == 'NWS Min T':

            file_path_1 = path+"/Night 1.png" 
            file_path_2 = path+"/Night 2.png" 
            file_path_3 = path+"/Night 3.png" 
            file_path_4 = path+"/Night 4.png" 
            file_path_5 = path+"/Night 5.png" 
            file_path_6 = path+"/Night 6.png" 
            file_path_7 = path+"/Night 7.png" 

            GIF = GIF_path+"/NWS Min T.gif"

            try:
                os.remove(file_path_1)
                os.remove(file_path_2)
                os.remove(file_path_3)
                os.remove(file_path_4)
                os.remove(file_path_5)
                os.remove(file_path_6)
                os.remove(file_path_7)
            except Exception as e:
                try:
                    os.remove(file_path_1)
                    os.remove(file_path_2)
                    os.remove(file_path_3)
                    os.remove(file_path_4)
                    os.remove(file_path_5)
                    os.remove(file_path_6)
                except Exception as e:
                    pass

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

        if plot_type == 'NWS Frost Freeze':

            file_path_1 = path+"/Night 1.png" 
            file_path_2 = path+"/Night 2.png" 
            file_path_3 = path+"/Night 3.png" 
            file_path_4 = path+"/Night 4.png" 
            file_path_5 = path+"/Night 5.png" 
            file_path_6 = path+"/Night 6.png" 
            file_path_7 = path+"/Night 7.png" 

            GIF = GIF_path+"/NWS Frost Freeze.gif"

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

        if plot_type == 'NWS Min T Trend':

            file_path_1 = path+"/Night 2.png" 
            file_path_2 = path+"/Night 3.png" 
            file_path_3 = path+"/Night 4.png" 
            file_path_4 = path+"/Night 5.png" 
            file_path_5 = path+"/Night 6.png" 
            file_path_6 = path+"/Night 7.png" 

            GIF = GIF_path+"/NWS Min T Trend.gif"

            try:
                os.remove(file_path_1)
                os.remove(file_path_2)
                os.remove(file_path_3)
                os.remove(file_path_4)
                os.remove(file_path_5)
                os.remove(file_path_6)
            except Exception as e:
                try:
                    os.remove(file_path_1)
                    os.remove(file_path_2)
                    os.remove(file_path_3)
                    os.remove(file_path_4)
                    os.remove(file_path_5)
                except Exception as e:
                    pass

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, None)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, None, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

        if plot_type == 'SPC CRITICAL FIRE WEATHER OUTLOOK':

            file_path_1 = path+"/Day 1.png" 
            file_path_2 = path+"/Day 2.png" 
            file_path_3 = path+"/Day 3.png" 
            file_path_4 = path+"/Day 4.png" 
            file_path_5 = path+"/Day 5.png" 
            file_path_6 = path+"/Day 6.png" 
            file_path_7 = path+"/Day 7.png" 

            GIF = GIF_path+"/SPC CRITICAL FIRE WEATHER OUTLOOK.gif"

            try:
                os.remove(file_path_1)
                os.remove(file_path_2)
                os.remove(file_path_3)
                os.remove(file_path_4)
                os.remove(file_path_5)
                os.remove(file_path_6)
                os.remove(file_path_7)
            except Exception as e:
                try:
                    os.remove(file_path_1)
                    os.remove(file_path_2)
                    os.remove(file_path_3)
                    os.remove(file_path_4)
                    os.remove(file_path_5)
                    os.remove(file_path_6)
                except Exception as e:
                    pass

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

        if plot_type == 'SPC DRY LIGHTNING OUTLOOK':

            file_path_1 = path+"/Day 1.png" 
            file_path_2 = path+"/Day 2.png" 
            file_path_3 = path+"/Day 3.png" 
            file_path_4 = path+"/Day 4.png" 
            file_path_5 = path+"/Day 5.png" 
            file_path_6 = path+"/Day 6.png" 
            file_path_7 = path+"/Day 7.png" 

            GIF = GIF_path+"/SPC DRY LIGHTNING OUTLOOK.gif"

            try:
                os.remove(file_path_1)
                os.remove(file_path_2)
                os.remove(file_path_3)
                os.remove(file_path_4)
                os.remove(file_path_5)
                os.remove(file_path_6)
                os.remove(file_path_7)
            except Exception as e:
                try:
                    os.remove(file_path_1)
                    os.remove(file_path_2)
                    os.remove(file_path_3)
                    os.remove(file_path_4)
                    os.remove(file_path_5)
                    os.remove(file_path_6)
                except Exception as e:
                    pass

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

    def save_daily_sounding_graphic(figure, station_id, date):

        station_id = station_id
        station_id = station_id.upper()
        fig = figure
        date = date
        

        if date == None:

            if os.path.exists(f"Weather Data"):
                print("Already Satisfied: Weather Data folder exists.")
                if os.path.exists(f"Weather Data/Soundings"):
                    print("Already Satisfied: Daily Weather Summary folder exists.")
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
                print("Already Satisfied: Weather Data folder exists.")
                if os.path.exists(f"Weather Data/Custom Date Soundings"):
                    print("Already Satisfied: Daily Weather Summary folder exists.")
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
            print("Already Satisfied: Weather Data folder exists.")
            if os.path.exists(f"Weather Data/Daily Weather Summary"):
                print("Already Satisfied: Daily Weather Summary folder exists.")
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
            
    def check_file_paths(state, gacc_region, plot_type, reference_system):

        state = state
        gacc_region = gacc_region
        plot_type = plot_type
        reference_system = reference_system

        if os.path.exists(f"Weather Data"):
            print("Already Satisfied: Weather Data folder exists.")
        else:
            print("Setting up the Weather Data folder and the rest of the file structure...")
            os.mkdir("Weather Data")

        if plot_type == 'SPC CRITICAL FIRE WEATHER OUTLOOK' or plot_type == 'SPC DRY LIGHTNING OUTLOOK':
            
            if state != None and gacc_region == None:

                state = state.upper()

                full_path = 'f:Weather Data/SPC Outlooks/'+plot_type+'/'+state+'/'+reference_system
                state_path = 'f:Weather Data/SPC Outlooks/'+plot_type+'/'+state
                type_path = 'f:Weather Data/SPC Outlooks/'+plot_type 

                full_path_gif = 'f:Weather Data/SPC Outlooks/GIFs/'+plot_type+'/'+state+'/'+reference_system
                state_path_gif = 'f:Weather Data/SPC Outlooks/GIFs/'+plot_type+'/'+state
                type_path_gif = 'f:Weather Data/SPC Outlooks/GIFs/'+plot_type

                if os.path.exists(f"Weather Data/SPC Outlooks"):
                    print("Already Satisfied: SPC Outlooks Directory exists.")

                    if os.path.exists(f"Weather Data/SPC Outlooks/{plot_type}"):
                        print('Already Satisfied: '+type_path+ ' exists.')
                        
                        if os.path.exists(f"Weather Data/SPC Outlooks/{plot_type}/{state}"):
                            print('Already Satisfied: '+state_path+' exists.')

                            if os.path.exists(f"Weather Data/SPC Outlooks/{plot_type}/{state}/{reference_system}"):
                                print('Already Satisfied: '+full_path+' exists')

                            else:
                                print(full_path+' not found. Automatically building new branch to directory...')
                                os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}/{state}/{reference_system}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(state_path+' not found. Automatically building new branch to directory...')
                            os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}/{state}/{reference_system}")
                            print("Successfully built new branch to directory!")
                            
                    else:
                        print(type_path+' not found. Automatically building new branch to directory...')
                        os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}")
                        os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}/{state}/{reference_system}")
                        print("Successfully built new branch to directory!")
                        
                else:
                    print("SPC Outlooks Directory does not exist.\nAutomatically building SPC Outlooks directory...")
                    
                    # Building directory for still images
                    os.mkdir(f"Weather Data/SPC Outlooks")
                    os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}")
                    os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}/{state}/{reference_system}")

                    print("Successfully built new directory!")

                ########################
                # GIF IMAGES DIRECTORY #
                ########################
                    
                if os.path.exists(f"Weather Data/SPC Outlooks"):
                    print("Already Satisfied: SPC Outlooks Directory exists.")

                    if os.path.exists(f"Weather Data/SPC Outlooks/GIFs/"):
                        print('Already Satisfied: SPC Outlooks GIFs Directory exists.')

                        if os.path.exists(f"Weather Data/SPC Outlooks/GIFs/{plot_type}"):
                            print('Already Satisfied: '+type_path_gif+ ' exists.')

                            if os.path.exists(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{state}"):
                                print('Already Satisfied: '+state_path_gif+ ' exists.')

                                if os.path.exists(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{state}/{reference_system}"):
                                    print('Already Satisfied: '+full_path_gif+ ' exists.')
                                else:
                                    os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{state}/{reference_system}")
                                    print("Successfully built new branch to directory!")   

                            else:
                                print(state_path_gif+' not found. Building branch to directory.')
                                os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{state}")
                                os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{state}/{reference_system}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(type_path_gif+' not found. Building branch to directory.')
                            os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}")
                            os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{state}/{reference_system}")
                            print("Successfully built new branch to directory!")
                            

                    else:
                        print('SPC Outlooks GIFs Directory not found. Building directory...')
                        os.mkdir(f"Weather Data/SPC Outlooks/GIFs/")
                        os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}")
                        os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{state}/{reference_system}")
                            
                        
                else:
                    print("SPC Outlooks Directory does not exist.\nAutomatically building SPC Outlooks directory...")
                    
                    # Building directory for still images
                    os.mkdir(f"Weather Data/SPC Outlooks")
                    os.mkdir(f"Weather Data/SPC Outlooks/GIFs/")
                    os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}")
                    os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{state}/{reference_system}")

                    print("Successfully built new directory!")

                path = f"Weather Data/SPC Outlooks/{plot_type}/{state}/{reference_system}"
                GIF_path = f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{state}/{reference_system}"

            if state == None and gacc_region != None:

                gacc_region = gacc_region.upper()
            
                full_path = 'f:Weather Data/SPC Outlooks/'+plot_type+'/'+gacc_region+'/'+reference_system
                gacc_path = 'f:Weather Data/SPC Outlooks/'+plot_type+'/'+gacc_region
                type_path = 'f:Weather Data/SPC Outlooks/'+plot_type

                full_path_gif = 'f:Weather Data/SPC Outlooks/GIFs/'+plot_type+'/'+gacc_region+'/'+reference_system
                gacc_path_gif = 'f:Weather Data/SPC Outlooks/GIFs/'+plot_type+'/'+gacc_region
                type_path_gif = 'f:Weather Data/SPC Outlooks/GIFs/'+plot_type


                ##########################
                # STILL IMAGES DIRECTORY #
                ##########################


                if os.path.exists(f"Weather Data/SPC Outlooks"):
                    print("Already Satisfied: SPC Outlooks Directory exists.")

                    if os.path.exists(f"Weather Data/SPC Outlooks/{plot_type}"):
                        print('Already Satisfied: '+type_path+ ' exists.')
                        
                        if os.path.exists(f"Weather Data/SPC Outlooks/{plot_type}/{gacc_region}"):
                            print('Already Satisfied: '+gacc_path+' exists.')

                            if os.path.exists(f"Weather Data/SPC Outlooks/{plot_type}/{gacc_region}/{reference_system}"):
                                print('Already Satisfied: '+full_path+' exists')

                            else:
                                print(full_path+' not found. Automatically building new branch to directory...')
                                os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}/{gacc_region}/{reference_system}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(gacc_path+' not found. Automatically building new branch to directory...')
                            os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}/{gacc_region}")
                            os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}/{gacc_region}/{reference_system}")
                            print("Successfully built new branch to directory!")
                            
                    else:
                        print(type_path+' not found. Automatically building new branch to directory...')
                        os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}")
                        os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}/{gacc_region}")
                        os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}/{gacc_region}/{reference_system}")
                        print("Successfully built new branch to directory!")
                        
                else:
                    print("SPC Outlooks Directory does not exist.\nAutomatically building SPC Outlooks directory...")
                    
                    # Building directory for still images
                    os.mkdir(f"Weather Data/SPC Outlooks")
                    os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}")
                    os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}/{gacc_region}")
                    os.mkdir(f"Weather Data/SPC Outlooks/{plot_type}/{gacc_region}/{reference_system}")

                    print("Successfully built new directory!")

                ########################
                # GIF IMAGES DIRECTORY #
                ########################
                    
                if os.path.exists(f"Weather Data/SPC Outlooks"):
                    print("Already Satisfied: SPC Outlooks Directory exists.")

                    if os.path.exists(f"Weather Data/SPC Outlooks/GIFs/"):
                        print('Already Satisfied: SPC Outlooks GIFs Directory exists.')

                        if os.path.exists(f"Weather Data/SPC Outlooks/GIFs/{plot_type}"):
                            print('Already Satisfied: '+type_path_gif+ ' exists.')

                            if os.path.exists(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{gacc_region}"):
                                print('Already Satisfied: '+gacc_path_gif+ ' exists.')

                                if os.path.exists(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{gacc_region}/{reference_system}"):
                                    print('Already Satisfied: '+full_path_gif+ ' exists.')
                                else:
                                    os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{gacc_region}/{reference_system}")
                                    print("Successfully built new branch to directory!")   

                            else:
                                print(gacc_path_gif+' not found. Building branch to directory.')
                                os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{gacc_region}")
                                os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{gacc_region}/{reference_system}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(type_path_gif+' not found. Building branch to directory.')
                            os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}")
                            os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{gacc_region}")
                            os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{gacc_region}/{reference_system}")
                            print("Successfully built new branch to directory!")
                            

                    else:
                        print('SPC Outlooks GIFs Directory not found. Building directory...')
                        os.mkdir(f"Weather Data/SPC Outlooks/GIFs/")
                        os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}")
                        os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{gacc_region}")
                        os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{gacc_region}/{reference_system}")
                            
                        
                else:
                    print("SPC Outlooks Directory does not exist.\nAutomatically building SPC Outlooks directory...")
                    
                    # Building directory for still images
                    os.mkdir(f"Weather Data/SPC Outlooks")
                    os.mkdir(f"Weather Data/SPC Outlooks/GIFs/")
                    os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}")
                    os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{gacc_region}")
                    os.mkdir(f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{gacc_region}/{reference_system}")

                    print("Successfully built new directory!")

                path = f"Weather Data/SPC Outlooks/{plot_type}/{gacc_region}/{reference_system}"
                GIF_path = f"Weather Data/SPC Outlooks/GIFs/{plot_type}/{gacc_region}/{reference_system}"

        if plot_type == 'RTMA RH' or plot_type =='24HR RTMA RH COMPARISON' or plot_type == 'RTMA TEMPERATURE' or plot_type == '24HR RTMA TEMPERATURE COMPARISON' or plot_type == '24HR RTMA TOTAL CLOUD COVER COMPARISON' or plot_type == 'RTMA TOTAL CLOUD COVER' or plot_type == '24HR RTMA DEW POINT COMPARISON' or plot_type == 'RTMA DEW POINT' or plot_type == 'RTMA WIND SPEED' or plot_type == '24HR RTMA WIND SPEED COMPARISON' or plot_type == '24HR RTMA WIND SPEED & DIRECTION COMPARISON WIND BARBS' or plot_type == '24HR RTMA WIND SPEED & DIRECTION COMPARISON WIND VECTORS' or plot_type == 'RTMA WIND SPEED & DIRECTION WIND VECTORS' or plot_type == 'RTMA WIND SPEED & DIRECTION WIND BARBS' or plot_type == 'RTMA DRY & WINDY AREAS SAMPLE POINTS' or plot_type == 'RTMA DRY & WINDY AREAS WIND BARBS' or plot_type == 'RTMA DRY & WINDY AREAS WIND VECTORS' or plot_type == 'RTMA DRY & GUSTY AREAS' or plot_type == 'RTMA RH & METAR' or plot_type == 'RTMA LOW RH & METAR' or plot_type == 'RTMA FROST FREEZE' or plot_type == 'RTMA EXTREME HEAT' or plot_type == 'RTMA TEMPERATURE ADVECTION' or plot_type == 'RTMA RH ADVECTION' or plot_type == 'RTMA DEW POINT ADVECTION' or plot_type == 'RTMA WIND GUST & OBS' or plot_type == 'RTMA WIND SPEED & OBS' or plot_type == 'RTMA LOW AND HIGH RH':

            if state != None and gacc_region == None:

                state = state.upper()

                full_path = 'f:Weather Data/RTMA/'+plot_type+'/'+state+'/'+reference_system
                state_path = 'f:Weather Data/RTMA/'+plot_type+'/'+state
                type_path = 'f:Weather Data/RTMA/'+plot_type

                if os.path.exists(f"Weather Data/RTMA"):
                    print("Already Satisfied: RTMA Directory exists.")

                    if os.path.exists(f"Weather Data/RTMA/{plot_type}"):
                        print('Already Satisfied: '+type_path+ ' exists.')
                        
                        if os.path.exists(f"Weather Data/RTMA/{plot_type}/{state}"):
                            print('Already Satisfied: '+state_path+' exists.')

                            if os.path.exists(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}"):
                                print('Already Satisfied: '+full_path+' exists')

                            else:
                                print(full_path+' not found. Automatically building new branch to directory...')
                                os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(state_path+' not found. Automatically building new branch to directory...')
                            os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                            print("Successfully built new branch to directory!")
                            
                    else:
                        print(type_path+' not found. Automatically building new branch to directory...')
                        os.mkdir(f"Weather Data/RTMA/{plot_type}")
                        os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                        print("Successfully built new branch to directory!")
                        
                else:
                    print("RTMA Directory does not exist.\nAutomatically building RTMA directory...")
                    
                    # Building directory for images
                    os.mkdir(f"Weather Data/RTMA")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")

                    print("Successfully built new directory!") 

                path = f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}"
                GIF_path = None

            if state == None and gacc_region != None:

                gacc_region = gacc_region.upper()

                full_path = 'f:Weather Data/RTMA/'+plot_type+'/'+gacc_region+'/'+reference_system
                gacc_path = 'f:Weather Data/RTMA/'+plot_type+'/'+gacc_region
                type_path = 'f:Weather Data/RTMA/'+plot_type

                if os.path.exists(f"Weather Data/RTMA"):
                    print("Already Satisfied: RTMA Directory exists.")

                    if os.path.exists(f"Weather Data/RTMA/{plot_type}"):
                        print('Already Satisfied: '+type_path+ ' exists.')
                        
                        if os.path.exists(f"Weather Data/RTMA/{plot_type}/{gacc_region}"):
                            print('Already Satisfied: '+gacc_path+' exists.')

                            if os.path.exists(f"Weather Data/RTMA/{plot_type}/{gacc_region}/{reference_system}"):
                                print('Already Satisfied: '+full_path+' exists')

                            else:
                                print(full_path+' not found. Automatically building new branch to directory...')
                                os.mkdir(f"Weather Data/RTMA/{plot_type}/{gacc_region}/{reference_system}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(gacc_path+' not found. Automatically building new branch to directory...')
                            os.mkdir(f"Weather Data/RTMA/{plot_type}/{gacc_region}")
                            os.mkdir(f"Weather Data/RTMA/{plot_type}/{gacc_region}/{reference_system}")
                            print("Successfully built new branch to directory!")
                            
                    else:
                        print(type_path+' not found. Automatically building new branch to directory...')
                        os.mkdir(f"Weather Data/RTMA/{plot_type}")
                        os.mkdir(f"Weather Data/RTMA/{plot_type}/{gacc_region}")
                        os.mkdir(f"Weather Data/RTMA/{plot_type}/{gacc_region}/{reference_system}")
                        print("Successfully built new branch to directory!")
                        
                else:
                    print("RTMA Directory does not exist.\nAutomatically building RTMA directory...")
                    
                    # Building directory for images
                    os.mkdir(f"Weather Data/RTMA")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{gacc_region}")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{gacc_region}/{reference_system}")

                    print("Successfully built new directory!") 

                path = f"Weather Data/RTMA/{plot_type}/{gacc_region}/{reference_system}"
                GIF_path = None

        if plot_type == 'NWS Low Minimum RH' or plot_type == 'NWS Poor Overnight Recovery' or plot_type == 'NWS Excellent Overnight Recovery' or plot_type == 'NWS Maximum RH' or plot_type == 'NWS Maximum RH Trend' or plot_type == 'NWS Minimum RH' or plot_type == 'NWS Minimum RH Trend' or plot_type == 'NWS Extreme Heat' or plot_type == 'NWS Max T Trend' or plot_type == 'NWS Warm Min T' or plot_type == 'NWS Frost Freeze' or plot_type == 'NWS Max T' or plot_type == 'NWS Min T' or plot_type == 'NWS Min T Trend':

            if state != None and gacc_region == None:

                state = state.upper()
            
                full_path = 'f:Weather Data/NWS Forecasts/'+plot_type+'/'+state+'/'+reference_system
                state_path = 'f:Weather Data/NWS Forecasts/'+plot_type+'/'+state
                type_path = 'f:Weather Data/NWS Forecasts/'+plot_type

                full_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type+'/'+state+'/'+reference_system
                state_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type+'/'+state
                type_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type


                ##########################
                # STILL IMAGES DIRECTORY #
                ##########################


                if os.path.exists(f"Weather Data/NWS Forecasts"):
                    print("Already Satisfied: NWS Forecasts Directory exists.")

                    if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}"):
                        print('Already Satisfied: '+type_path+ ' exists.')
                        
                        if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}/{state}"):
                            print('Already Satisfied: '+state_path+' exists.')

                            if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}"):
                                print('Already Satisfied: '+full_path+' exists')

                            else:
                                print(full_path+' not found. Automatically building new branch to directory...')
                                os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(state_path+' not found. Automatically building new branch to directory...')
                            os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                            print("Successfully built new branch to directory!")
                            
                    else:
                        print(type_path+' not found. Automatically building new branch to directory...')
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}")
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                        print("Successfully built new branch to directory!")
                        
                else:
                    print("NWS Forecasts Directory does not exist.\nAutomatically building NWS Forecasts directory...")
                    
                    # Building directory for still images
                    os.mkdir(f"Weather Data/NWS Forecasts")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")

                    print("Successfully built new directory!")

                ########################
                # GIF IMAGES DIRECTORY #
                ########################
                    
                if os.path.exists(f"Weather Data/NWS Forecasts"):
                    print("Already Satisfied: NWS Forecasts Directory exists.")

                    if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/"):
                        print('Already Satisfied: NWS Forecasts GIFs Directory exists.')

                        if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}"):
                            print('Already Satisfied: '+type_path_gif+ ' exists.')

                            if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}"):
                                print('Already Satisfied: '+state_path_gif+ ' exists.')

                                if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}"):
                                    print('Already Satisfied: '+full_path_gif+ ' exists.')
                                else:
                                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                                    print("Successfully built new branch to directory!")   

                            else:
                                print(state_path_gif+' not found. Building branch to directory.')
                                os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                                os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(type_path_gif+' not found. Building branch to directory.')
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                            print("Successfully built new branch to directory!")
                            

                    else:
                        print('NWS Forecasts GIFs Directory not found. Building directory...')
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                            
                        
                else:
                    print("NWS Forecasts Directory does not exist.\nAutomatically building NWS Forecasts directory...")
                    
                    # Building directory for still images
                    os.mkdir(f"Weather Data/NWS Forecasts")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")

                    print("Successfully built new directory!")

                path = f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}"
                GIF_path = f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}"

            if state == None and gacc_region != None:

                gacc_region = gacc_region.upper()
            
                full_path = 'f:Weather Data/NWS Forecasts/'+plot_type+'/'+gacc_region+'/'+reference_system
                gacc_path = 'f:Weather Data/NWS Forecasts/'+plot_type+'/'+gacc_region
                type_path = 'f:Weather Data/NWS Forecasts/'+plot_type

                full_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type+'/'+gacc_region+'/'+reference_system
                gacc_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type+'/'+gacc_region
                type_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type


                ##########################
                # STILL IMAGES DIRECTORY #
                ##########################


                if os.path.exists(f"Weather Data/NWS Forecasts"):
                    print("Already Satisfied: NWS Forecasts Directory exists.")

                    if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}"):
                        print('Already Satisfied: '+type_path+ ' exists.')
                        
                        if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}/{gacc_region}"):
                            print('Already Satisfied: '+gacc_path+' exists.')

                            if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}/{gacc_region}/{reference_system}"):
                                print('Already Satisfied: '+full_path+' exists')

                            else:
                                print(full_path+' not found. Automatically building new branch to directory...')
                                os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{gacc_region}/{reference_system}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(gacc_path+' not found. Automatically building new branch to directory...')
                            os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{gacc_region}")
                            os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{gacc_region}/{reference_system}")
                            print("Successfully built new branch to directory!")
                            
                    else:
                        print(type_path+' not found. Automatically building new branch to directory...')
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}")
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{gacc_region}")
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{gacc_region}/{reference_system}")
                        print("Successfully built new branch to directory!")
                        
                else:
                    print("NWS Forecasts Directory does not exist.\nAutomatically building NWS Forecasts directory...")
                    
                    # Building directory for still images
                    os.mkdir(f"Weather Data/NWS Forecasts")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{gacc_region}")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{gacc_region}/{reference_system}")

                    print("Successfully built new directory!")

                ########################
                # GIF IMAGES DIRECTORY #
                ########################
                    
                if os.path.exists(f"Weather Data/NWS Forecasts"):
                    print("Already Satisfied: NWS Forecasts Directory exists.")

                    if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/"):
                        print('Already Satisfied: NWS Forecasts GIFs Directory exists.')

                        if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}"):
                            print('Already Satisfied: '+type_path_gif+ ' exists.')

                            if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{gacc_region}"):
                                print('Already Satisfied: '+gacc_path_gif+ ' exists.')

                                if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{gacc_region}/{reference_system}"):
                                    print('Already Satisfied: '+full_path_gif+ ' exists.')
                                else:
                                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{gacc_region}/{reference_system}")
                                    print("Successfully built new branch to directory!")   

                            else:
                                print(gacc_path_gif+' not found. Building branch to directory.')
                                os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{gacc_region}")
                                os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{gacc_region}/{reference_system}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(type_path_gif+' not found. Building branch to directory.')
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{gacc_region}")
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{gacc_region}/{reference_system}")
                            print("Successfully built new branch to directory!")
                            

                    else:
                        print('NWS Forecasts GIFs Directory not found. Building directory...')
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{gacc_region}")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{gacc_region}/{reference_system}")
                            
                        
                else:
                    print("NWS Forecasts Directory does not exist.\nAutomatically building NWS Forecasts directory...")
                    
                    # Building directory for still images
                    os.mkdir(f"Weather Data/NWS Forecasts")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{gacc_region}")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{gacc_region}/{reference_system}")

                    print("Successfully built new directory!")

                path = f"Weather Data/NWS Forecasts/{plot_type}/{gacc_region}/{reference_system}"
                GIF_path = f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{gacc_region}/{reference_system}"
                    

        return path, GIF_path


    def check_file_paths_alaska(state, cwa, plot_type, reference_system):
    
        state = state
        cwa = cwa
        plot_type = plot_type
        reference_system = reference_system
        state = state.upper()
        if cwa != None:
            cwa = cwa.upper()
    
        if os.path.exists(f"Weather Data"):
            print("Already Satisfied: Weather Data folder exists.")
        else:
            print("Setting up the Weather Data folder and the rest of the file structure...")
            os.mkdir("Weather Data")
    
        if plot_type == 'RTMA RH' or plot_type =='24HR RTMA RH COMPARISON' or plot_type == 'RTMA TEMPERATURE' or plot_type == '24HR RTMA TEMPERATURE COMPARISON' or plot_type == '24HR RTMA TOTAL CLOUD COVER COMPARISON' or plot_type == 'RTMA TOTAL CLOUD COVER' or plot_type == '24HR RTMA DEW POINT COMPARISON' or plot_type == 'RTMA DEW POINT' or plot_type == 'RTMA WIND SPEED' or plot_type == '24HR RTMA WIND SPEED COMPARISON' or plot_type == '24HR RTMA WIND SPEED & DIRECTION COMPARISON WIND BARBS' or plot_type == '24HR RTMA WIND SPEED & DIRECTION COMPARISON WIND VECTORS' or plot_type == 'RTMA WIND SPEED & DIRECTION WIND VECTORS' or plot_type == 'RTMA WIND SPEED & DIRECTION WIND BARBS' or plot_type == 'RTMA HOT DRY & WINDY AREAS SAMPLE POINTS' or plot_type == 'RTMA HOT DRY & WINDY AREAS WIND BARBS' or plot_type == 'RTMA HOT DRY & WINDY AREAS WIND VECTORS' or plot_type == 'RTMA HOT DRY & GUSTY AREAS' or plot_type == 'RTMA RH & METAR' or plot_type == 'RTMA LOW RH & METAR' or plot_type == 'RTMA FROST FREEZE' or plot_type == 'RTMA EXTREME HEAT' or plot_type == 'RTMA TEMPERATURE ADVECTION' or plot_type == 'RTMA RH ADVECTION' or plot_type == 'RTMA DEW POINT ADVECTION' or plot_type == 'RTMA WIND GUST & OBS' or plot_type == 'RTMA WIND SPEED & OBS' or plot_type == 'RTMA LOW AND HIGH RH':
    
            if cwa == None:
    
                full_path = 'f:Weather Data/RTMA/'+plot_type+'/'+state+'/'+reference_system+'/STATE'
                ref_path = 'f:Weather Data/RTMA/'+plot_type+'/'+state+'/'+reference_system
                state_path = 'f:Weather Data/RTMA/'+plot_type+'/'+state
                type_path = 'f:Weather Data/RTMA/'+plot_type
    
                if os.path.exists(f"Weather Data/RTMA"):
                    print("Already Satisfied: RTMA Directory exists.")
    
                    if os.path.exists(f"Weather Data/RTMA/{plot_type}"):
                        print('Already Satisfied: '+type_path+ ' exists.')
                        
                        if os.path.exists(f"Weather Data/RTMA/{plot_type}/{state}"):
                            print('Already Satisfied: '+state_path+' exists.')
    
                            if os.path.exists(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}"):
                                print('Already Satisfied: '+ref_path+' exists')

                                if os.path.exists(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/STATE"):
                                    print('Already Satisfied: '+full_path+' exists')

                                else:
                                    print(full_path+' not found. Automatically building new branch to directory...')
                                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/STATE")
                                    print("Successfully built new branch to directory!")  
    
                            else:
                                print(ref_path+' not found. Automatically building new branch to directory...')
                                os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                                os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/STATE")
                                print("Successfully built new branch to directory!")                                
    
                        else:
                            print(state_path+' not found. Automatically building new branch to directory...')
                            os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                            os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/STATE")
                            print("Successfully built new branch to directory!")
                            
                    else:
                        print(type_path+' not found. Automatically building new branch to directory...')
                        os.mkdir(f"Weather Data/RTMA/{plot_type}")
                        os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                        os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/STATE")
                        print("Successfully built new branch to directory!")
                        
                else:
                    print("RTMA Directory does not exist.\nAutomatically building RTMA directory...")
                    
                    # Building directory for images
                    os.mkdir(f"Weather Data/RTMA")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/STATE")
    
                    print("Successfully built new directory!") 
    
                path = f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/STATE"
                GIF_path = None
    
            if cwa != None:
    
                full_path = 'f:Weather Data/RTMA/'+plot_type+'/'+state+'/'+reference_system+'/'+cwa
                ref_path = 'f:Weather Data/RTMA/'+plot_type+'/'+state+'/'+reference_system
                state_path = 'f:Weather Data/RTMA/'+plot_type+'/'+state
                type_path = 'f:Weather Data/RTMA/'+plot_type
    
                if os.path.exists(f"Weather Data/RTMA"):
                    print("Already Satisfied: RTMA Directory exists.")
    
                    if os.path.exists(f"Weather Data/RTMA/{plot_type}"):
                        print('Already Satisfied: '+type_path+ ' exists.')
                        
                        if os.path.exists(f"Weather Data/RTMA/{plot_type}/{state}"):
                            print('Already Satisfied: '+state_path+' exists.')
    
                            if os.path.exists(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}"):
                                print('Already Satisfied: '+ref_path+' exists')
    
                                if os.path.exists(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/{cwa}"):
                                    print('Already Satisfied: '+full_path+' exists')
    
                                else:
                                    print(full_path+' not found. Automatically building new branch to directory...')
                                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/{cwa}")                                    
                            else:
                                print(ref_path+' not found. Automatically building new branch to directory...')
                                os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                                os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/{cwa}") 
                                print("Successfully built new branch to directory!")                                
    
                        else:
                            print(state_path+' not found. Automatically building new branch to directory...')
                            os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                            os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/{cwa}") 
                            print("Successfully built new branch to directory!")
                            
                    else:
                        print(type_path+' not found. Automatically building new branch to directory...')
                        os.mkdir(f"Weather Data/RTMA/{plot_type}")
                        os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                        os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/{cwa}") 
                        print("Successfully built new branch to directory!")
                        
                else:
                    print("RTMA Directory does not exist.\nAutomatically building RTMA directory...")
                    
                    # Building directory for images
                    os.mkdir(f"Weather Data/RTMA")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/{cwa}") 
                    print("Successfully built new directory!") 
    
                path = f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/{cwa}"
                GIF_path = None
    
    
        if plot_type == 'NWS Low Minimum RH' or plot_type == 'NWS Poor Overnight Recovery' or plot_type == 'NWS Excellent Overnight Recovery' or plot_type == 'NWS Maximum RH' or plot_type == 'NWS Maximum RH Trend' or plot_type == 'NWS Minimum RH' or plot_type == 'NWS Minimum RH Trend' or plot_type == 'NWS Extreme Heat' or plot_type == 'NWS Max T Trend' or plot_type == 'NWS Warm Min T' or plot_type == 'NWS Frost Freeze' or plot_type == 'NWS Max T' or plot_type == 'NWS Min T' or plot_type == 'NWS Min T Trend':

            if cwa != None:

                full_path = 'f:Weather Data/NWS Forecasts/'+plot_type+'/'+state+'/'+reference_system+'/'+cwa
                ref_path = 'f:Weather Data/NWS Forecasts/'+plot_type+'/'+state+'/'+reference_system
                state_path = 'f:Weather Data/NWS Forecasts/'+plot_type+'/'+state
                type_path = 'f:Weather Data/NWS Forecasts/'+plot_type

                full_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type+'/'+state+'/'+reference_system+'/'+cwa
                ref_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type+'/'+state+'/'+reference_system
                state_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type+'/'+state
                type_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type


                ##########################
                # STILL IMAGES DIRECTORY #
                ##########################


                if os.path.exists(f"Weather Data/NWS Forecasts"):
                    print("Already Satisfied: NWS Forecasts Directory exists.")

                    if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}"):
                        print('Already Satisfied: '+type_path+ ' exists.')
                        
                        if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}/{state}"):
                            print('Already Satisfied: '+state_path+' exists.')

                            if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}"):
                                print('Already Satisfied: '+full_path+' exists')

                                if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{cwa}"):
                                    print('Already Satisfied: '+full_path+' exists')

                                else:
                                    print(full_path+' not found. Automatically building new branch to directory...')
                                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{cwa}")
                                    print("Successfully built new branch to directory!")    

                            else:
                                print(ref_path+' not found. Automatically building new branch to directory...')
                                os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                                os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{cwa}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(state_path+' not found. Automatically building new branch to directory...')
                            os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                            os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{cwa}")
                            print("Successfully built new branch to directory!")
                            
                    else:
                        print(type_path+' not found. Automatically building new branch to directory...')
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}")
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{cwa}")
                        print("Successfully built new branch to directory!")
                        
                else:
                    print("NWS Forecasts Directory does not exist.\nAutomatically building NWS Forecasts directory...")
                    
                    # Building directory for still images
                    os.mkdir(f"Weather Data/NWS Forecasts")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{cwa}")

                    print("Successfully built new directory!")

                ########################
                # GIF IMAGES DIRECTORY #
                ########################
                    
                if os.path.exists(f"Weather Data/NWS Forecasts"):
                    print("Already Satisfied: NWS Forecasts Directory exists.")

                    if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/"):
                        print('Already Satisfied: NWS Forecasts GIFs Directory exists.')

                        if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}"):
                            print('Already Satisfied: '+type_path_gif+ ' exists.')

                            if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}"):
                                print('Already Satisfied: '+state_path_gif+ ' exists.')

                                if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}"):
                                    print('Already Satisfied: '+ref_path_gif+ ' exists.')
                                    
                                    if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{cwa}"):
                                        print('Already Satisfied: '+full_path_gif+ ' exists.')

                                    else:
                                        print(f"{full_path_gif} not found. Building new branch to directory.")
                                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{cwa}")
                                        print("Successfully built new branch to directory!")                                           

                                else:
                                    print(f"{ref_path_gif} not found. Building new branch to directory.")
                                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{cwa}")
                                    print("Successfully built new branch to directory!")   

                            else:
                                print(state_path_gif+' not found. Building branch to directory.')
                                os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                                os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                                os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{cwa}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(type_path_gif+' not found. Building branch to directory.')
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{cwa}")
                            print("Successfully built new branch to directory!")
                            

                    else:
                        print('NWS Forecasts GIFs Directory not found. Building directory...')
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{cwa}")
                            
                        
                else:
                    print("NWS Forecasts Directory does not exist.\nAutomatically building NWS Forecasts directory...")
                    
                    # Building directory for still images
                    os.mkdir(f"Weather Data/NWS Forecasts")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{cwa}")

                    print("Successfully built new directory!")

                path = f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{cwa}"
                GIF_path = f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{cwa}"                    
            if cwa == None:

                cwa = 'STATE'
            
                ##########################
                # STILL IMAGES DIRECTORY #
                ##########################

                full_path = 'f:Weather Data/NWS Forecasts/'+plot_type+'/'+state+'/'+reference_system+'/'+cwa
                ref_path = 'f:Weather Data/NWS Forecasts/'+plot_type+'/'+state+'/'+reference_system
                state_path = 'f:Weather Data/NWS Forecasts/'+plot_type+'/'+state
                type_path = 'f:Weather Data/NWS Forecasts/'+plot_type

                full_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type+'/'+state+'/'+reference_system+'/'+cwa
                ref_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type+'/'+state+'/'+reference_system
                state_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type+'/'+state
                type_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type


                if os.path.exists(f"Weather Data/NWS Forecasts"):
                    print("Already Satisfied: NWS Forecasts Directory exists.")

                    if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}"):
                        print('Already Satisfied: '+type_path+ ' exists.')
                        
                        if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}/{state}"):
                            print('Already Satisfied: '+state_path+' exists.')

                            if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}"):
                                print('Already Satisfied: '+full_path+' exists')

                                if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{cwa}"):
                                    print('Already Satisfied: '+full_path+' exists')

                                else:
                                    print(full_path+' not found. Automatically building new branch to directory...')
                                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{cwa}")
                                    print("Successfully built new branch to directory!")    

                            else:
                                print(ref_path+' not found. Automatically building new branch to directory...')
                                os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                                os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{cwa}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(state_path+' not found. Automatically building new branch to directory...')
                            os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                            os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{cwa}")
                            print("Successfully built new branch to directory!")
                            
                    else:
                        print(type_path+' not found. Automatically building new branch to directory...')
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}")
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{cwa}")
                        print("Successfully built new branch to directory!")
                        
                else:
                    print("NWS Forecasts Directory does not exist.\nAutomatically building NWS Forecasts directory...")
                    
                    # Building directory for still images
                    os.mkdir(f"Weather Data/NWS Forecasts")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{cwa}")

                    print("Successfully built new directory!")

                ########################
                # GIF IMAGES DIRECTORY #
                ########################
                    
                if os.path.exists(f"Weather Data/NWS Forecasts"):
                    print("Already Satisfied: NWS Forecasts Directory exists.")

                    if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/"):
                        print('Already Satisfied: NWS Forecasts GIFs Directory exists.')

                        if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}"):
                            print('Already Satisfied: '+type_path_gif+ ' exists.')

                            if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}"):
                                print('Already Satisfied: '+state_path_gif+ ' exists.')

                                if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}"):
                                    print('Already Satisfied: '+ref_path_gif+ ' exists.')
                                    
                                    if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{cwa}"):
                                        print('Already Satisfied: '+full_path_gif+ ' exists.')

                                    else:
                                        print(f"{full_path_gif} not found. Building new branch to directory.")
                                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{cwa}")
                                        print("Successfully built new branch to directory!")                                           

                                else:
                                    print(f"{ref_path_gif} not found. Building new branch to directory.")
                                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{cwa}")
                                    print("Successfully built new branch to directory!")   

                            else:
                                print(state_path_gif+' not found. Building branch to directory.')
                                os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                                os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                                os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{cwa}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(type_path_gif+' not found. Building branch to directory.')
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{cwa}")
                            print("Successfully built new branch to directory!")
                            

                    else:
                        print('NWS Forecasts GIFs Directory not found. Building directory...')
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{cwa}")                            
                        
                else:
                    print("NWS Forecasts Directory does not exist.\nAutomatically building NWS Forecasts directory...")
                    
                    # Building directory for still images
                    os.mkdir(f"Weather Data/NWS Forecasts")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{cwa}")

                    print("Successfully built new directory!")

                path = f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{cwa}"
                GIF_path = f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{cwa}" 

        return path, GIF_path

    def check_file_paths_hawaii(state, island, plot_type, reference_system):
    
        state = state
        island = island
        plot_type = plot_type
        reference_system = reference_system
        state = state.upper()
        if island != None:
            island = island.upper()
    
        if os.path.exists(f"Weather Data"):
            print("Already Satisfied: Weather Data folder exists.")
        else:
            print("Setting up the Weather Data folder and the rest of the file structure...")
            os.mkdir("Weather Data")
    
        if plot_type == 'RTMA RH' or plot_type =='24HR RTMA RH COMPARISON' or plot_type == 'RTMA TEMPERATURE' or plot_type == '24HR RTMA TEMPERATURE COMPARISON' or plot_type == '24HR RTMA TOTAL CLOUD COVER COMPARISON' or plot_type == 'RTMA TOTAL CLOUD COVER' or plot_type == '24HR RTMA DEW POINT COMPARISON' or plot_type == 'RTMA DEW POINT' or plot_type == 'RTMA WIND SPEED' or plot_type == '24HR RTMA WIND SPEED COMPARISON' or plot_type == '24HR RTMA WIND SPEED & DIRECTION COMPARISON WIND BARBS' or plot_type == '24HR RTMA WIND SPEED & DIRECTION COMPARISON WIND VECTORS' or plot_type == 'RTMA WIND SPEED & DIRECTION WIND VECTORS' or plot_type == 'RTMA WIND SPEED & DIRECTION WIND BARBS' or plot_type == 'RTMA HOT DRY & WINDY AREAS SAMPLE POINTS' or plot_type == 'RTMA HOT DRY & WINDY AREAS WIND BARBS' or plot_type == 'RTMA HOT DRY & WINDY AREAS WIND VECTORS' or plot_type == 'RTMA HOT DRY & GUSTY AREAS' or plot_type == 'RTMA RH & METAR' or plot_type == 'RTMA LOW RH & METAR' or plot_type == 'RTMA FROST FREEZE' or plot_type == 'RTMA EXTREME HEAT' or plot_type == 'RTMA TEMPERATURE ADVECTION' or plot_type == 'RTMA RH ADVECTION' or plot_type == 'RTMA DEW POINT ADVECTION' or plot_type == 'RTMA WIND GUST & OBS' or plot_type == 'RTMA WIND SPEED & OBS' or plot_type == 'RTMA LOW AND HIGH RH':
    
            if island == None:
    
                full_path = 'f:Weather Data/RTMA/'+plot_type+'/'+state+'/'+reference_system+'/STATE'
                ref_path = 'f:Weather Data/RTMA/'+plot_type+'/'+state+'/'+reference_system
                state_path = 'f:Weather Data/RTMA/'+plot_type+'/'+state
                type_path = 'f:Weather Data/RTMA/'+plot_type
    
                if os.path.exists(f"Weather Data/RTMA"):
                    print("Already Satisfied: RTMA Directory exists.")
    
                    if os.path.exists(f"Weather Data/RTMA/{plot_type}"):
                        print('Already Satisfied: '+type_path+ ' exists.')
                        
                        if os.path.exists(f"Weather Data/RTMA/{plot_type}/{state}"):
                            print('Already Satisfied: '+state_path+' exists.')
    
                            if os.path.exists(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}"):
                                print('Already Satisfied: '+ref_path+' exists')

                                if os.path.exists(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/STATE"):
                                    print('Already Satisfied: '+full_path+' exists')

                                else:
                                    print(full_path+' not found. Automatically building new branch to directory...')
                                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/STATE")
                                    print("Successfully built new branch to directory!")  
    
                            else:
                                print(ref_path+' not found. Automatically building new branch to directory...')
                                os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                                os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/STATE")
                                print("Successfully built new branch to directory!")                                
    
                        else:
                            print(state_path+' not found. Automatically building new branch to directory...')
                            os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                            os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/STATE")
                            print("Successfully built new branch to directory!")
                            
                    else:
                        print(type_path+' not found. Automatically building new branch to directory...')
                        os.mkdir(f"Weather Data/RTMA/{plot_type}")
                        os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                        os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/STATE")
                        print("Successfully built new branch to directory!")
                        
                else:
                    print("RTMA Directory does not exist.\nAutomatically building RTMA directory...")
                    
                    # Building directory for images
                    os.mkdir(f"Weather Data/RTMA")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/STATE")
    
                    print("Successfully built new directory!") 
    
                path = f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/STATE"
                GIF_path = None
    
            if island != None:
    
                full_path = 'f:Weather Data/RTMA/'+plot_type+'/'+state+'/'+reference_system+'/'+island
                ref_path = 'f:Weather Data/RTMA/'+plot_type+'/'+state+'/'+reference_system
                state_path = 'f:Weather Data/RTMA/'+plot_type+'/'+state
                type_path = 'f:Weather Data/RTMA/'+plot_type
    
                if os.path.exists(f"Weather Data/RTMA"):
                    print("Already Satisfied: RTMA Directory exists.")
    
                    if os.path.exists(f"Weather Data/RTMA/{plot_type}"):
                        print('Already Satisfied: '+type_path+ ' exists.')
                        
                        if os.path.exists(f"Weather Data/RTMA/{plot_type}/{state}"):
                            print('Already Satisfied: '+state_path+' exists.')
    
                            if os.path.exists(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}"):
                                print('Already Satisfied: '+ref_path+' exists')
    
                                if os.path.exists(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/{island}"):
                                    print('Already Satisfied: '+full_path+' exists')
    
                                else:
                                    print(full_path+' not found. Automatically building new branch to directory...')
                                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/{island}")                                    
                            else:
                                print(ref_path+' not found. Automatically building new branch to directory...')
                                os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                                os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/{island}") 
                                print("Successfully built new branch to directory!")                                
    
                        else:
                            print(state_path+' not found. Automatically building new branch to directory...')
                            os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                            os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/{island}") 
                            print("Successfully built new branch to directory!")
                            
                    else:
                        print(type_path+' not found. Automatically building new branch to directory...')
                        os.mkdir(f"Weather Data/RTMA/{plot_type}")
                        os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                        os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/{island}") 
                        print("Successfully built new branch to directory!")
                        
                else:
                    print("RTMA Directory does not exist.\nAutomatically building RTMA directory...")
                    
                    # Building directory for images
                    os.mkdir(f"Weather Data/RTMA")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}")
                    os.mkdir(f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/{island}") 
                    print("Successfully built new directory!") 
    
                path = f"Weather Data/RTMA/{plot_type}/{state}/{reference_system}/{island}"
                GIF_path = None
    
    
        if plot_type == 'NWS Low Minimum RH' or plot_type == 'NWS Poor Overnight Recovery' or plot_type == 'NWS Excellent Overnight Recovery' or plot_type == 'NWS Maximum RH' or plot_type == 'NWS Maximum RH Trend' or plot_type == 'NWS Minimum RH' or plot_type == 'NWS Minimum RH Trend' or plot_type == 'NWS Extreme Heat' or plot_type == 'NWS Max T Trend' or plot_type == 'NWS Warm Min T' or plot_type == 'NWS Frost Freeze' or plot_type == 'NWS Max T' or plot_type == 'NWS Min T' or plot_type == 'NWS Min T Trend':

            if island != None:

                full_path = 'f:Weather Data/NWS Forecasts/'+plot_type+'/'+state+'/'+reference_system+'/'+island
                ref_path = 'f:Weather Data/NWS Forecasts/'+plot_type+'/'+state+'/'+reference_system
                state_path = 'f:Weather Data/NWS Forecasts/'+plot_type+'/'+state
                type_path = 'f:Weather Data/NWS Forecasts/'+plot_type

                full_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type+'/'+state+'/'+reference_system+'/'+island
                ref_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type+'/'+state+'/'+reference_system
                state_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type+'/'+state
                type_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type


                ##########################
                # STILL IMAGES DIRECTORY #
                ##########################


                if os.path.exists(f"Weather Data/NWS Forecasts"):
                    print("Already Satisfied: NWS Forecasts Directory exists.")

                    if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}"):
                        print('Already Satisfied: '+type_path+ ' exists.')
                        
                        if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}/{state}"):
                            print('Already Satisfied: '+state_path+' exists.')

                            if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}"):
                                print('Already Satisfied: '+full_path+' exists')

                                if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{island}"):
                                    print('Already Satisfied: '+full_path+' exists')

                                else:
                                    print(full_path+' not found. Automatically building new branch to directory...')
                                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{island}")
                                    print("Successfully built new branch to directory!")    

                            else:
                                print(ref_path+' not found. Automatically building new branch to directory...')
                                os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                                os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{island}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(state_path+' not found. Automatically building new branch to directory...')
                            os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                            os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{island}")
                            print("Successfully built new branch to directory!")
                            
                    else:
                        print(type_path+' not found. Automatically building new branch to directory...')
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}")
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{island}")
                        print("Successfully built new branch to directory!")
                        
                else:
                    print("NWS Forecasts Directory does not exist.\nAutomatically building NWS Forecasts directory...")
                    
                    # Building directory for still images
                    os.mkdir(f"Weather Data/NWS Forecasts")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{island}")

                    print("Successfully built new directory!")

                ########################
                # GIF IMAGES DIRECTORY #
                ########################
                    
                if os.path.exists(f"Weather Data/NWS Forecasts"):
                    print("Already Satisfied: NWS Forecasts Directory exists.")

                    if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/"):
                        print('Already Satisfied: NWS Forecasts GIFs Directory exists.')

                        if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}"):
                            print('Already Satisfied: '+type_path_gif+ ' exists.')

                            if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}"):
                                print('Already Satisfied: '+state_path_gif+ ' exists.')

                                if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}"):
                                    print('Already Satisfied: '+ref_path_gif+ ' exists.')
                                    
                                    if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{island}"):
                                        print('Already Satisfied: '+full_path_gif+ ' exists.')

                                    else:
                                        print(f"{full_path_gif} not found. Building new branch to directory.")
                                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{island}")
                                        print("Successfully built new branch to directory!")                                           

                                else:
                                    print(f"{ref_path_gif} not found. Building new branch to directory.")
                                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{island}")
                                    print("Successfully built new branch to directory!")   

                            else:
                                print(state_path_gif+' not found. Building branch to directory.')
                                os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                                os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                                os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{island}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(type_path_gif+' not found. Building branch to directory.')
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{island}")
                            print("Successfully built new branch to directory!")
                            

                    else:
                        print('NWS Forecasts GIFs Directory not found. Building directory...')
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{island}")
                            
                        
                else:
                    print("NWS Forecasts Directory does not exist.\nAutomatically building NWS Forecasts directory...")
                    
                    # Building directory for still images
                    os.mkdir(f"Weather Data/NWS Forecasts")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{island}")

                    print("Successfully built new directory!")

                path = f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{island}"
                GIF_path = f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{island}"                    
            if island == None:

                island = 'STATE'
            
                ##########################
                # STILL IMAGES DIRECTORY #
                ##########################

                full_path = 'f:Weather Data/NWS Forecasts/'+plot_type+'/'+state+'/'+reference_system+'/'+island
                ref_path = 'f:Weather Data/NWS Forecasts/'+plot_type+'/'+state+'/'+reference_system
                state_path = 'f:Weather Data/NWS Forecasts/'+plot_type+'/'+state
                type_path = 'f:Weather Data/NWS Forecasts/'+plot_type

                full_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type+'/'+state+'/'+reference_system+'/'+island
                ref_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type+'/'+state+'/'+reference_system
                state_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type+'/'+state
                type_path_gif = 'f:Weather Data/NWS Forecasts/GIFs/'+plot_type


                if os.path.exists(f"Weather Data/NWS Forecasts"):
                    print("Already Satisfied: NWS Forecasts Directory exists.")

                    if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}"):
                        print('Already Satisfied: '+type_path+ ' exists.')
                        
                        if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}/{state}"):
                            print('Already Satisfied: '+state_path+' exists.')

                            if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}"):
                                print('Already Satisfied: '+full_path+' exists')

                                if os.path.exists(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{island}"):
                                    print('Already Satisfied: '+full_path+' exists')

                                else:
                                    print(full_path+' not found. Automatically building new branch to directory...')
                                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{island}")
                                    print("Successfully built new branch to directory!")    

                            else:
                                print(ref_path+' not found. Automatically building new branch to directory...')
                                os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                                os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{island}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(state_path+' not found. Automatically building new branch to directory...')
                            os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                            os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{island}")
                            print("Successfully built new branch to directory!")
                            
                    else:
                        print(type_path+' not found. Automatically building new branch to directory...')
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}")
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                        os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{island}")
                        print("Successfully built new branch to directory!")
                        
                else:
                    print("NWS Forecasts Directory does not exist.\nAutomatically building NWS Forecasts directory...")
                    
                    # Building directory for still images
                    os.mkdir(f"Weather Data/NWS Forecasts")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}")
                    os.mkdir(f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{island}")

                    print("Successfully built new directory!")

                ########################
                # GIF IMAGES DIRECTORY #
                ########################
                    
                if os.path.exists(f"Weather Data/NWS Forecasts"):
                    print("Already Satisfied: NWS Forecasts Directory exists.")

                    if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/"):
                        print('Already Satisfied: NWS Forecasts GIFs Directory exists.')

                        if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}"):
                            print('Already Satisfied: '+type_path_gif+ ' exists.')

                            if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}"):
                                print('Already Satisfied: '+state_path_gif+ ' exists.')

                                if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}"):
                                    print('Already Satisfied: '+ref_path_gif+ ' exists.')
                                    
                                    if os.path.exists(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{island}"):
                                        print('Already Satisfied: '+full_path_gif+ ' exists.')

                                    else:
                                        print(f"{full_path_gif} not found. Building new branch to directory.")
                                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{island}")
                                        print("Successfully built new branch to directory!")                                           

                                else:
                                    print(f"{ref_path_gif} not found. Building new branch to directory.")
                                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{island}")
                                    print("Successfully built new branch to directory!")   

                            else:
                                print(state_path_gif+' not found. Building branch to directory.')
                                os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                                os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                                os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{island}")
                                print("Successfully built new branch to directory!")                                

                        else:
                            print(type_path_gif+' not found. Building branch to directory.')
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                            os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{island}")
                            print("Successfully built new branch to directory!")
                            

                    else:
                        print('NWS Forecasts GIFs Directory not found. Building directory...')
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                        os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{island}")                            
                        
                else:
                    print("NWS Forecasts Directory does not exist.\nAutomatically building NWS Forecasts directory...")
                    
                    # Building directory for still images
                    os.mkdir(f"Weather Data/NWS Forecasts")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}")
                    os.mkdir(f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{island}")

                    print("Successfully built new directory!")

                path = f"Weather Data/NWS Forecasts/{plot_type}/{state}/{reference_system}/{island}"
                GIF_path = f"Weather Data/NWS Forecasts/GIFs/{plot_type}/{state}/{reference_system}/{island}" 

        return path, GIF_path


class save:

    r'''
    This class hosts the function that parses through a figure list and saves the figures to a specified file location

    '''

    def save_image(file_path):

        plt.savefig(file_path, bbox_inches='tight')

    def extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7):

        r'''
        This function extracts indivdual figures from a list of figures and saves them with a specified file path. 
        *This function is only to be used for the NWS NDFD plots and/or SPC Fire Weather Outlook Graphics.* 

        Inputs: 1) figure_list (List) - List of figures returned by the plotting function. 
                2) file_path_1 (String) - Path to where the first figure is saved. 
                3) file_path_2 (String) - Path to where the second figure is saved. 
                4) file_path_3 (String) - Path to where the third figure is saved. 
                5) file_path_4 (String) - Path to where the fourth figure is saved.
                6) file_path_5 (String) - Path to where the fifth figure is saved.
                7) file_path_6 (String) - Path to where the sixth figure is saved.
                7) file_path_7 (String) - Path to where the seventh figure is saved.

        Return: Each figure in the list is saved as its own file to a specified file path

        '''
        try:
            fig1 = figure_list[0]
            fig1 = fig1.savefig(file_path_1, bbox_inches='tight')
            plt.close(fig1)
            fig2 = figure_list[1]
            fig2 = fig2.savefig(file_path_2, bbox_inches='tight')
            plt.close(fig2)
            fig3 = figure_list[2]
            fig3 = fig3.savefig(file_path_3, bbox_inches='tight')
            plt.close(fig3)
            fig4 = figure_list[3]
            fig4 = fig4.savefig(file_path_4, bbox_inches='tight')
            plt.close(fig4) 
            fig5 = figure_list[4]
            fig5 = fig5.savefig(file_path_5, bbox_inches='tight')
            plt.close(fig5) 
            fig6 = figure_list[5]
            fig6 = fig6.savefig(file_path_6, bbox_inches='tight')
            plt.close(fig6) 
            fig7 = figure_list[6]
            fig7 = fig7.savefig(file_path_7, bbox_inches='tight')
            plt.close(fig7)
            print("All frames saved.")
        except Exception as ee:
            try:
                fig1 = figure_list[0]
                fig1 = fig1.savefig(file_path_1, bbox_inches='tight')
                plt.close(fig1)
                fig2 = figure_list[1]
                fig2 = fig2.savefig(file_path_2, bbox_inches='tight')
                plt.close(fig2)
                fig3 = figure_list[2]
                fig3 = fig3.savefig(file_path_3, bbox_inches='tight')
                plt.close(fig3)
                fig4 = figure_list[3]
                fig4 = fig4.savefig(file_path_4, bbox_inches='tight')
                plt.close(fig4) 
                fig5 = figure_list[4]
                fig5 = fig5.savefig(file_path_5, bbox_inches='tight')
                plt.close(fig5) 
                fig6 = figure_list[5]
                fig6 = fig6.savefig(file_path_6, bbox_inches='tight')
                plt.close(fig6) 
                print("All frames saved.")
            except Exception as a:
                try:
                    fig1 = figure_list[0]
                    fig1 = fig1.savefig(file_path_1, bbox_inches='tight')
                    plt.close(fig1)
                    fig2 = figure_list[1]
                    fig2 = fig2.savefig(file_path_2, bbox_inches='tight')
                    plt.close(fig2)
                    fig3 = figure_list[2]
                    fig3 = fig3.savefig(file_path_3, bbox_inches='tight')
                    plt.close(fig3)
                    fig4 = figure_list[3]
                    fig4 = fig4.savefig(file_path_4, bbox_inches='tight')
                    plt.close(fig4) 
                    fig5 = figure_list[4]
                    fig5 = fig5.savefig(file_path_5, bbox_inches='tight')
                    plt.close(fig5)
                    print("All frames saved.")
                except Exception as b:    
                    try:
                        fig1 = figure_list[0]
                        fig1 = fig1.savefig(file_path_1, bbox_inches='tight')
                        plt.close(fig1)
                        fig2 = figure_list[1]
                        fig2 = fig2.savefig(file_path_2, bbox_inches='tight')
                        plt.close(fig2)
                        fig3 = figure_list[2]
                        fig3 = fig3.savefig(file_path_3, bbox_inches='tight')
                        plt.close(fig3)
                        fig4 = figure_list[3]
                        fig4 = fig4.savefig(file_path_4, bbox_inches='tight')
                        plt.close(fig4)
                        print("All frames saved.")
                    except Exception as c:
                        try:     
                            fig1 = figure_list[0]
                            fig1 = fig1.savefig(file_path_1, bbox_inches='tight')
                            plt.close(fig1)
                            fig2 = figure_list[1]
                            fig2 = fig2.savefig(file_path_2, bbox_inches='tight')
                            plt.close(fig2)
                            fig3 = figure_list[2]
                            fig3 = fig3.savefig(file_path_3, bbox_inches='tight')
                            plt.close(fig3)
                            print("All frames saved.")
                        except Exception as b:
                            try:
                                fig1 = figure_list[0]
                                fig1 = fig1.savefig(file_path_1, bbox_inches='tight')
                                plt.close(fig1)
                                fig2 = figure_list[1]
                                fig2 = fig2.savefig(file_path_2, bbox_inches='tight')
                                plt.close(fig2)
                                print("All frames saved.")
                            except Exception as c:
                                try:
                                    fig1 = figure_list[0]
                                    fig1 = fig1.savefig(file_path_1, bbox_inches='tight')
                                    plt.close(fig1)
                                    print("All frames saved.")
                                except Exception as d:
                                    pass    


    def make_NDFD_Outlook_GIF(GIF_Image_file_path, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, file_path_8, fps=1):

        r'''
        This function makes an animated GIF images of the NWS/NDFD plots and/or SPC Outlooks and saves the GIF to a specified location. 
        *This function is only to be used for the NWS NDFD plots and/or SPC Fire Weather Outlook Graphics.* 
        
        Inputs: 1) GIF_Image_file_path (String) - The path to where the GIF image saves to plus the filename of the GIF image. 
                2) file_path_1 (String) - Path to where the first figure is saved. 
                3) file_path_2 (String) - Path to where the second figure is saved. 
                4) file_path_3 (String) - Path to where the third figure is saved. 
                5) file_path_4 (String) - Path to where the fourth figure is saved.
                6) file_path_5 (String) - Path to where the fifth figure is saved.
                7) file_path_6 (String) - Path to where the sixth figure is saved.
                8) file_path_7 (String) - Path to where the seventh figure is saved.
                9) file_path_8 (String) - Path to where the eigth figure is saved.
                10) fps (Integer) - The rate in frames per second the GIF loops. 

        '''


        try:
            file_path_1 = file_path_1
            file_path_2 = file_path_2
            file_path_3 = file_path_3
            file_path_4 = file_path_4
            file_path_5 = file_path_5
            file_path_6 = file_path_6
            file_path_7 = file_path_7
            file_path_8 = file_path_8

            datetime_str_1 = time.ctime(os.path.getmtime(file_path_1))
            datetime_str_2 = time.ctime(os.path.getmtime(file_path_2))
            datetime_str_3 = time.ctime(os.path.getmtime(file_path_3))
            datetime_str_4 = time.ctime(os.path.getmtime(file_path_4))
            datetime_str_5 = time.ctime(os.path.getmtime(file_path_5))
            datetime_str_6 = time.ctime(os.path.getmtime(file_path_6))
            datetime_str_7 = time.ctime(os.path.getmtime(file_path_7))
            datetime_str_8 = time.ctime(os.path.getmtime(file_path_8))

            day_1 = datetime.strptime(datetime_str_1, '%a %b %d %H:%M:%S %Y')
            day_2 = datetime.strptime(datetime_str_2, '%a %b %d %H:%M:%S %Y')
            day_3 = datetime.strptime(datetime_str_3, '%a %b %d %H:%M:%S %Y')
            day_4 = datetime.strptime(datetime_str_4, '%a %b %d %H:%M:%S %Y')
            day_5 = datetime.strptime(datetime_str_5, '%a %b %d %H:%M:%S %Y')
            day_6 = datetime.strptime(datetime_str_6, '%a %b %d %H:%M:%S %Y')
            day_7 = datetime.strptime(datetime_str_7, '%a %b %d %H:%M:%S %Y')
            day_8 = datetime.strptime(datetime_str_8, '%a %b %d %H:%M:%S %Y')
        
            if day_7.day == day_8.day and day_7.hour == day_8.hour:
                filenames = []
                filenames.append(file_path_1)
                filenames.append(file_path_2)
                filenames.append(file_path_3)
                filenames.append(file_path_4)
                filenames.append(file_path_5)
                filenames.append(file_path_6)
                filenames.append(file_path_7)
                filenames.append(file_path_8)

            else:
                filenames = []
                filenames.append(file_path_1)
                filenames.append(file_path_2)
                filenames.append(file_path_3)
                filenames.append(file_path_4)
                filenames.append(file_path_5)
                filenames.append(file_path_6)
                filenames.append(file_path_7)  
            
            with imageio.get_writer(GIF_Image_file_path, fps=fps) as writer:
                for filename in filenames:
                    image = imageio.v2.imread(filename)
                    writer.append_data(image)
                    
            
        except Exception as a:
            try:
                file_path_1 = file_path_1
                file_path_2 = file_path_2
                file_path_3 = file_path_3
                file_path_4 = file_path_4
                file_path_5 = file_path_5
                file_path_6 = file_path_6
                file_path_7 = file_path_7
                
    
                datetime_str_1 = time.ctime(os.path.getmtime(file_path_1))
                datetime_str_2 = time.ctime(os.path.getmtime(file_path_2))
                datetime_str_3 = time.ctime(os.path.getmtime(file_path_3))
                datetime_str_4 = time.ctime(os.path.getmtime(file_path_4))
                datetime_str_5 = time.ctime(os.path.getmtime(file_path_5))
                datetime_str_6 = time.ctime(os.path.getmtime(file_path_6))
                datetime_str_7 = time.ctime(os.path.getmtime(file_path_7))
    
                day_1 = datetime.strptime(datetime_str_1, '%a %b %d %H:%M:%S %Y')
                day_2 = datetime.strptime(datetime_str_2, '%a %b %d %H:%M:%S %Y')
                day_3 = datetime.strptime(datetime_str_3, '%a %b %d %H:%M:%S %Y')
                day_4 = datetime.strptime(datetime_str_4, '%a %b %d %H:%M:%S %Y')
                day_5 = datetime.strptime(datetime_str_5, '%a %b %d %H:%M:%S %Y')
                day_6 = datetime.strptime(datetime_str_6, '%a %b %d %H:%M:%S %Y')
                day_7 = datetime.strptime(datetime_str_7, '%a %b %d %H:%M:%S %Y')
            
                if day_6.day == day_7.day and day_6.hour == day_7.hour:
                    filenames = []
                    filenames.append(file_path_1)
                    filenames.append(file_path_2)
                    filenames.append(file_path_3)
                    filenames.append(file_path_4)
                    filenames.append(file_path_5)
                    filenames.append(file_path_6)
                    filenames.append(file_path_7)
    
                else:
                    filenames = []
                    filenames.append(file_path_1)
                    filenames.append(file_path_2)
                    filenames.append(file_path_3)
                    filenames.append(file_path_4)
                    filenames.append(file_path_5)
                    filenames.append(file_path_6)

                with imageio.get_writer(GIF_Image_file_path, fps=fps) as writer:
                    for filename in filenames:
                        image = imageio.v2.imread(filename)
                        writer.append_data(image)
        
            except Exception as b:
                try:
                    file_path_1 = file_path_1
                    file_path_2 = file_path_2
                    file_path_3 = file_path_3
                    file_path_4 = file_path_4
                    file_path_5 = file_path_5
                    file_path_6 = file_path_6
        
                    datetime_str_1 = time.ctime(os.path.getmtime(file_path_1))
                    datetime_str_2 = time.ctime(os.path.getmtime(file_path_2))
                    datetime_str_3 = time.ctime(os.path.getmtime(file_path_3))
                    datetime_str_4 = time.ctime(os.path.getmtime(file_path_4))
                    datetime_str_5 = time.ctime(os.path.getmtime(file_path_5))
                    datetime_str_6 = time.ctime(os.path.getmtime(file_path_6))
        
                    day_1 = datetime.strptime(datetime_str_1, '%a %b %d %H:%M:%S %Y')
                    day_2 = datetime.strptime(datetime_str_2, '%a %b %d %H:%M:%S %Y')
                    day_3 = datetime.strptime(datetime_str_3, '%a %b %d %H:%M:%S %Y')
                    day_4 = datetime.strptime(datetime_str_4, '%a %b %d %H:%M:%S %Y')
                    day_5 = datetime.strptime(datetime_str_5, '%a %b %d %H:%M:%S %Y')
                    day_6 = datetime.strptime(datetime_str_6, '%a %b %d %H:%M:%S %Y')
                
                    if day_5.day == day_6.day and day_5.hour == day_6.hour:
                        filenames = []
                        filenames.append(file_path_1)
                        filenames.append(file_path_2)
                        filenames.append(file_path_3)
                        filenames.append(file_path_4)
                        filenames.append(file_path_5)
                        filenames.append(file_path_6)
                  
                    else:
                        filenames = []
                        filenames.append(file_path_1)
                        filenames.append(file_path_2)
                        filenames.append(file_path_3)
                        filenames.append(file_path_4)
                        filenames.append(file_path_5)
                    
                    with imageio.get_writer(GIF_Image_file_path, fps=fps) as writer:
                        for filename in filenames:
                            image = imageio.v2.imread(filename)
                            writer.append_data(image)

                except Exception as c:

                    file_path_1 = file_path_1
                    file_path_2 = file_path_2
                    file_path_3 = file_path_3
                    file_path_4 = file_path_4
                    file_path_5 = file_path_5
        
                    datetime_str_1 = time.ctime(os.path.getmtime(file_path_1))
                    datetime_str_2 = time.ctime(os.path.getmtime(file_path_2))
                    datetime_str_3 = time.ctime(os.path.getmtime(file_path_3))
                    datetime_str_4 = time.ctime(os.path.getmtime(file_path_4))
                    datetime_str_5 = time.ctime(os.path.getmtime(file_path_5))
        
                    day_1 = datetime.strptime(datetime_str_1, '%a %b %d %H:%M:%S %Y')
                    day_2 = datetime.strptime(datetime_str_2, '%a %b %d %H:%M:%S %Y')
                    day_3 = datetime.strptime(datetime_str_3, '%a %b %d %H:%M:%S %Y')
                    day_4 = datetime.strptime(datetime_str_4, '%a %b %d %H:%M:%S %Y')
                    day_5 = datetime.strptime(datetime_str_5, '%a %b %d %H:%M:%S %Y')
                
                    if day_4.day == day_5.day and day_4.hour == day_5.hour:
                        filenames = []
                        filenames.append(file_path_1)
                        filenames.append(file_path_2)
                        filenames.append(file_path_3)
                        filenames.append(file_path_4)
                        filenames.append(file_path_5)
                  
                    else:
                        filenames = []
                        filenames.append(file_path_1)
                        filenames.append(file_path_2)
                        filenames.append(file_path_3)
                        filenames.append(file_path_4)
                    
                    with imageio.get_writer(GIF_Image_file_path, fps=fps) as writer:
                        for filename in filenames:
                            image = imageio.v2.imread(filename)
                            writer.append_data(image)                  
            
        
        
    def extract_RTMA_figures_6hr_timelapse(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7):

        r'''
        This function extracts indivdual figures from a list of figures and saves them with a specified file path. 
        *This function is only to be used for the RTMA Graphics.* 

        Inputs: 1) figure_list (List) - List of figures returned by the plotting function. 
                2) file_path_1 (String) - Path to where the first figure is saved. 
                3) file_path_2 (String) - Path to where the second figure is saved. 
                4) file_path_3 (String) - Path to where the third figure is saved. 
                5) file_path_4 (String) - Path to where the fourth figure is saved.
                6) file_path_5 (String) - Path to where the fifth figure is saved.
                7) file_path_6 (String) - Path to where the sixth figure is saved.
                8) file_path_7 (String) - Path to where the seventh figure is saved.

        Return: Each figure in the list is saved as its own file to a specified file path

        '''
        try:
            fig1 = figure_list[0]
            fig1 = fig1.savefig(file_path_1, bbox_inches='tight')
            plt.close(fig1)
            fig2 = figure_list[1]
            fig2 = fig2.savefig(file_path_2, bbox_inches='tight')
            plt.close(fig2)
            fig3 = figure_list[2]
            fig3 = fig3.savefig(file_path_3, bbox_inches='tight')
            plt.close(fig3)
            fig4 = figure_list[3]
            fig4 = fig4.savefig(file_path_4, bbox_inches='tight')
            plt.close(fig4) 
            fig5 = figure_list[4]
            fig5 = fig5.savefig(file_path_5, bbox_inches='tight')
            plt.close(fig5) 
            fig6 = figure_list[5]
            fig6 = fig6.savefig(file_path_6, bbox_inches='tight')
            plt.close(fig6) 
            fig7 = figure_list[6]
            fig7 = fig7.savefig(file_path_7, bbox_inches='tight')
            plt.close(fig7)

        except Exception as a:
            try:
                fig1 = figure_list[0]
                fig1 = fig1.savefig(file_path_1, bbox_inches='tight')
                plt.close(fig1)
                fig2 = figure_list[1]
                fig2 = fig2.savefig(file_path_2, bbox_inches='tight')
                plt.close(fig2)
                fig3 = figure_list[2]
                fig3 = fig3.savefig(file_path_3, bbox_inches='tight')
                plt.close(fig3)
                fig4 = figure_list[3]
                fig4 = fig4.savefig(file_path_4, bbox_inches='tight')
                plt.close(fig4) 
                fig5 = figure_list[4]
                fig5 = fig5.savefig(file_path_5, bbox_inches='tight')
                plt.close(fig5) 
                fig6 = figure_list[5]
                fig6 = fig6.savefig(file_path_6, bbox_inches='tight')
                plt.close(fig6) 
    
            except Exception as b:
                try:
                    fig1 = figure_list[0]
                    fig1 = fig1.savefig(file_path_1, bbox_inches='tight')
                    plt.close(fig1)
                    fig2 = figure_list[1]
                    fig2 = fig2.savefig(file_path_2, bbox_inches='tight')
                    plt.close(fig2)
                    fig3 = figure_list[2]
                    fig3 = fig3.savefig(file_path_3, bbox_inches='tight')
                    plt.close(fig3)
                    fig4 = figure_list[3]
                    fig4 = fig4.savefig(file_path_4, bbox_inches='tight')
                    plt.close(fig4) 
                    fig5 = figure_list[4]
                    fig5 = fig5.savefig(file_path_5, bbox_inches='tight')
                    plt.close(fig5)
                except Exception as c:    
                    try:
                        fig1 = figure_list[0]
                        fig1 = fig1.savefig(file_path_1, bbox_inches='tight')
                        plt.close(fig1)
                        fig2 = figure_list[1]
                        fig2 = fig2.savefig(file_path_2, bbox_inches='tight')
                        plt.close(fig2)
                        fig3 = figure_list[2]
                        fig3 = fig3.savefig(file_path_3, bbox_inches='tight')
                        plt.close(fig3)
                        fig4 = figure_list[3]
                        fig4 = fig4.savefig(file_path_4, bbox_inches='tight')
                        plt.close(fig4)
                    
                    except Exception as d:
                        try:     
                            fig1 = figure_list[0]
                            fig1 = fig1.savefig(file_path_1, bbox_inches='tight')
                            plt.close(fig1)
                            fig2 = figure_list[1]
                            fig2 = fig2.savefig(file_path_2, bbox_inches='tight')
                            plt.close(fig2)
                            fig3 = figure_list[2]
                            fig3 = fig3.savefig(file_path_3, bbox_inches='tight')
                            plt.close(fig3)
                
                        except Exception as e:
                            try:
                                fig1 = figure_list[0]
                                fig1 = fig1.savefig(file_path_1, bbox_inches='tight')
                                plt.close(fig1)
                                fig2 = figure_list[1]
                                fig2 = fig2.savefig(file_path_2, bbox_inches='tight')
                                plt.close(fig2)
                
                            except Exception as f:
                                try:
                                    fig1 = figure_list[0]
                                    fig1 = fig1.savefig(file_path_1, bbox_inches='tight')
                                    plt.close(fig1)
                
                                except Exception as g:
                                    pass        


    def make_RTMA_6hr_timelapse_GIF(GIF_Image_file_path, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7, fps=1):

        r'''
        This function makes an animated GIF images of the SPC Outlooks and saves the GIF to a specified location. 

        Inputs: 1) GIF_Image_file_path (String) - The path to where the GIF image saves to plus the filename of the GIF image. 
                2) file_path_1 (String) - Path to where the first figure is saved. 
                3) file_path_2 (String) - Path to where the second figure is saved. 
                4) file_path_3 (String) - Path to where the third figure is saved. 
                5) file_path_4 (String) - Path to where the fourth figure is saved.
                6) file_path_5 (String) - Path to where the fifth figure is saved.
                7) file_path_6 (String) - Path to where the sixth figure is saved.
                8) file_path_7 (String) - Path to where the seventh figure is saved.
                9) fps (Integer) - The rate in frames per second the GIF loops. 

        '''


        filenames = []
        filenames.append(file_path_1)
        filenames.append(file_path_2)
        filenames.append(file_path_3)
        filenames.append(file_path_4)
        filenames.append(file_path_5)
        filenames.append(file_path_6)
        filenames.append(file_path_7)


        try:
            with imageio.get_writer(GIF_Image_file_path, fps=fps) as writer:
                for filename in filenames:
                    image = imageio.v2.imread(filename)
                    writer.append_data(image)
        
        except Exception as a:
            try:
                with imageio.get_writer(GIF_Image_file_path, fps=fps) as writer:
                    new_list = []
                    image_1 = filenames[0]
                    image_2 = filenames[1]
                    image_3 = filenames[2]
                    image_4 = filenames[3]
                    image_5 = filenames[4]
                    image_6 = filenames[5]
                    image_7 = filenames[6]
                    new_list.append(image_1)
                    new_list.append(image_2)
                    new_list.append(image_3)
                    new_list.append(image_4)
                    new_list.append(image_5)
                    new_list.append(image_6)
                    new_list.append(image_7)
            
                    for filename in new_list:
                        image = imageio.v2.imread(filename)
                        writer.append_data(image)
                        
            
        
            except Exception as b:
                with imageio.get_writer(GIF_Image_file_path, fps=fps) as writer:
                    new_list = []
                    image_1 = filenames[0]
                    image_2 = filenames[1]
                    image_3 = filenames[2]
                    image_4 = filenames[3]
                    image_5 = filenames[4]
                    image_6 = filenames[5]
                    new_list.append(image_1)
                    new_list.append(image_2)
                    new_list.append(image_3)
                    new_list.append(image_4)
                    new_list.append(image_5)
                    new_list.append(image_6)
            
                    for filename in new_list:
                        image = imageio.v2.imread(filename)
                        writer.append_data(image)        
        
        print("GIF Saved!")   


    def clear_NDFD_images(file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, file_path_7):


        file_path_1 = file_path_1
        file_path_2 = file_path_2
        file_path_3 = file_path_3
        file_path_4 = file_path_4
        file_path_5 = file_path_5
        file_path_6 = file_path_6
        file_path_7 = file_path_7

        

        try:
            os.remove(file_path_1)
            print("First File Removed.")
        except Exception as a:
            print("File doesn't exist")

        try:
            os.remove(file_path_2)
            print("Second File Removed.")
        except Exception as b:
            print("File doesn't exist")

        try:
            os.remove(file_path_3)
            print("Third File Removed.")
        except Exception as c:
            print("File doesn't exist")

        try:
            os.remove(file_path_4)
            print("Fourth File Removed.")
        except Exception as d:
            print("File doesn't exist")

        try:
            os.remove(file_path_5)
            print("Fifth File Removed.")
        except Exception as e:
            print("File doesn't exist")

        try:
            os.remove(file_path_6)
            print("Sixth File Removed.")
        except Exception as f:
            print("File doesn't exist")

        try:
            os.remove(file_path_7)
            print("Seventh File Removed.")
        except Exception as g:
            print("File doesn't exist")


    def append_data_RTMA_6hr_timelapse(rtma_data_1, rtma_data_2, rtma_data_3, rtma_data_4, rtma_data_5, rtma_data_6, rtma_data_7, rtma_data_8, rtma_time_1, rtma_time_2, rtma_time_3, rtma_time_4, rtma_time_5, rtma_time_6, rtma_time_7, rtma_time_8):


        rtma_data_1 = rtma_data_1
        rtma_data_2 = rtma_data_2 
        rtma_data_3 = rtma_data_3 
        rtma_data_4 = rtma_data_4
        rtma_data_5 = rtma_data_5 
        rtma_data_6 = rtma_data_6 
        rtma_data_7 = rtma_data_7 
        rtma_time_1 = rtma_time_1
        rtma_time_2 = rtma_time_2
        rtma_time_3 = rtma_time_3
        rtma_time_4 = rtma_time_4
        rtma_time_5 = rtma_time_5 
        rtma_time_6 = rtma_time_6
        rtma_time_7 = rtma_time_7
        rtma_time_8 = rtma_time_8

        data = []
        data.append(rtma_data_1)
        data.append(rtma_data_2)
        data.append(rtma_data_3)
        data.append(rtma_data_4)
        data.append(rtma_data_5)
        data.append(rtma_data_6)
        data.append(rtma_data_7)
        data.append(rtma_data_8)

        times = []
        times.append(rtma_time_1)
        times.append(rtma_time_2)
        times.append(rtma_time_3)
        times.append(rtma_time_4)
        times.append(rtma_time_5)
        times.append(rtma_time_6)
        times.append(rtma_time_7)
        times.append(rtma_time_8)

        return data, times
