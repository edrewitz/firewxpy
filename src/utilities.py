import os
import imageio
import matplotlib.pyplot as plt
import time
from zipfile import ZipFile
from PIL import Image
from datetime import datetime, timedelta

class file_functions:

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

        if plot_type == 'NWS Maximum RH Trend':

            file_path_1 = path+"/Night 2.png" 
            file_path_2 = path+"/Night 3.png" 
            file_path_3 = path+"/Night 4.png" 
            file_path_4 = path+"/Night 5.png" 
            file_path_5 = path+"/Night 6.png" 
            file_path_6 = path+"/Night 7.png" 

            GIF = GIF_path+"/NWS Maximum RH Trend.gif"

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

            save.extract_NDFD_figures(figure_list, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, None)

            save.make_NDFD_Outlook_GIF(GIF, file_path_1, file_path_2, file_path_3, file_path_4, file_path_5, file_path_6, None, None)

            print("Individual images saved to: "+path)
            print("GIF saved to "+GIF_path)

            
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
                        except Exception as b:
                            try:
                                fig1 = figure_list[0]
                                fig1 = fig1.savefig(file_path_1, bbox_inches='tight')
                                plt.close(fig1)
                                fig2 = figure_list[1]
                                fig2 = fig2.savefig(file_path_2, bbox_inches='tight')
                                plt.close(fig2)
                            except Exception as c:
                                try:
                                    fig1 = figure_list[0]
                                    fig1 = fig1.savefig(file_path_1, bbox_inches='tight')
                                    plt.close(fig1)
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
