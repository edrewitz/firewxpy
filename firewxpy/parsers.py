# THIS SCRIPT HAS FUNCTIONS THAT PARSE THROUGH GRIB FILES THAT CONTAIN WEATHER DATA TO RETURN SORTED AND ORGANIZED DATA ARRAYS FOR GRAPHICAL CREATION/PLOTTING
#
# DEPENDENCIES INCLUDE:
# 1. PYGRIB
# 2. DATETIME 
#
#  (C) METEOROLOGIST ERIC J. DREWITZ
#               USDA/USFS

##### IMPORTS NEEDED PYTHON MODULES #######

import pygrib
import numpy as np
import firewxpy.data_access as da
import matplotlib.pyplot as plt
import firewxpy.calc as calc
import cartopy.crs as ccrs
import xarray as xr
import os
import warnings
warnings.filterwarnings('ignore')

from datetime import datetime, timedelta
from metpy.units import units


class NDFD:

    r'''
    THIS CLASS HOSTS A VARIETY OF FUNCTIONS TO PARSE THROUGH THE NWS NDFD GRIB DATA

    '''

    def figure_count(figure_list):
    
        figure_list = figure_list
        for i in figure_list:
            i = i + 1
            return i

    def grib_to_xarray(file):
        
        try:
            ds = xr.open_dataset(file, engine='cfgrib')
            ds = ds.metpy.parse_cf()
            ds1 = None
            print("Extracted the data successfully.")
            stepUnits = False
        except Exception as e:
            print("Unsuccessful data extraction. Likely an issue with stepUnits. Retrying!")
            ds = xr.open_dataset(file, engine='cfgrib', filter_by_keys={'stepUnits': 0})
            ds1 = xr.open_dataset(file, engine='cfgrib', filter_by_keys={'stepUnits': 1})
            ds = ds.metpy.parse_cf()
            ds1 = ds1.metpy.parse_cf()
            print("Extracted the data successfully.")
            stepUnits = True
        return ds, ds1, stepUnits


    def ndfd_step_count(ds_short, ds_extended):

        ds_short = ds_short
        ds_extended = ds_extended

        try:
            if ds_short['step'][3]:
                print("There are 4 short-term step intervals.")
                short_steps = 4
        except Exception as e:
            try:
                if ds_short['step'][2]:
                    print("There are 3 short-term step intervals.")
                    short_steps = 3
            except Exception as e:
                try:
                    if ds_short['step'][1]:
                        print("There are 2 short-term step intervals.")
                        short_steps = 2
                except Exception as e:
                    print("There is 1 short-term step interval.")
                    short_steps = 1
        
        try:
            if ds_extended['step'][4]:
                print("There are 5 extended step intervals.")
                extended_steps = 5
        except Exception as e:
            try:
                if ds_extended['step'][3]:
                    print("There are 4 extended step intervals.")
                    extended_steps = 4
            except Exception as e:
                try:
                    if ds_extended['step'][2]:
                        print("There are 3 extended step intervals.")
                        extended_steps = 3
                except Exception as e:
                    try:
                        if ds_extended['step'][1]:
                            print("There are 2 extended step intervals.")
                            extended_steps = 2
                    except Exception as e:
                        print("There is 1 extended step interval.")
                        extended_steps = 1
        
        steps = short_steps + extended_steps  
        print(f"There are {steps} total time steps.")
        
        return steps, short_steps, extended_steps


    def parse_GRIB_files_full_forecast_period(file_path, grid_time_interval, convert_temperature, count_short, count_extended, directory_name):

        GRIB_File_List = pygrib.open(file_path)
        grid_time_interval = grid_time_interval
        convert_temperature = convert_temperature
        count_short = count_short
        count_extended = count_extended
        directory_name = directory_name

        utc = datetime.utcnow()
        local = datetime.now()

        utc_hour = utc.hour
        local_hour = local.hour

        if file_path != 'ds.apt.bin' or file_path != 'ds.conhazo.bin' or file_path != 'ds.critfireo.bin' or file_path != 'ds.dryfireo.bin' or file_path != 'ds.iceaccum.bin' or file_path != 'ds.maxrh.bin' or file_path != 'ds.maxt.bin' or file_path != 'ds.minrh.bin' or file_path != 'ds.mint.bin' or file_path != 'ds.phail.bin' or file_path != 'ds.pop12.bin' or file_path != 'ds.ptornado.bin' or file_path != 'ds.ptotsvrtstm.bin' or file_path != 'ds.ptotxsvrtstm.bin' or file_path != 'ds.ptstmwinds.bin' or file_path != 'ds.pxhail.bin' or file_path != 'ds.pxtornado.bin' or file_path != 'ds.pxtstmwinds.bin' or file_path != 'ds.qpf.bin' or file_path != 'ds.rhm.bin' or file_path != 'ds.sky.bin' or file_path != 'ds.snow.bin' or file_path != 'ds.tcwspdabv34c.bin' or file_path != 'ds.tcwspdabv34i.bin' or file_path != 'ds.tcwspdabv50c.bin' or file_path != 'ds.tcwspdabv50i.bin' or file_path != 'ds.tcwspdabv64c.bin' or file_path != 'ds.tcwspdabv64i.bin' or file_path != 'ds.td.bin' or file_path != 'ds.temp.bin' or file_path != 'ds.waveh.bin' or file_path != 'ds.wdir.bin' or file_path != 'ds.wgust.bin' or file_path != 'ds.wspd.bin' or file_path != 'ds.wwa.bin' or file_path != 'ds.wx.bin':

            file_path = os.path.basename(file_path)

        else:
            file_path = file_path

        count = 0
        for grb in GRIB_File_List:
            count = count + 1

        print("There are " +str(count) + " GRIB files in the " + file_path + " download.\n")

        if file_path == 'ds.minrh.bin' or file_path == 'ds.maxrh.bin' or file_path == 'ds.critfireo.bin' or file_path == 'ds.dryfireo.bin':
    
            if count == 5: 
                grb_1 = GRIB_File_List[1]
                grb_2 = GRIB_File_List[2]
                grb_3 = GRIB_File_List[3]
                grb_4 = GRIB_File_List[4]
                grb_5 = GRIB_File_List[5]
                grb_6 = None
                grb_7 = None
                grb_8 = None
    
                grb_1_vals = grb_1.values
                grb_1_start = grb_1.validDate
                grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                grb_2_vals = grb_2.values
                grb_2_start = grb_2.validDate
                grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                grb_3_vals = grb_3.values
                grb_3_start = grb_3.validDate
                grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                grb_4_vals = grb_4.values
                grb_4_start = grb_4.validDate
                grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
                grb_5_vals = grb_5.values
                grb_5_start = grb_5.validDate
                grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
                grb_6_vals = None
                grb_6_start = None
                grb_6_end = None
                grb_7_vals = None
                grb_7_start = None
                grb_7_end = None
                grb_8_vals = None
                grb_8_start = None
                grb_8_end = None
                
                          
                lats_1, lons_1 = grb_1.latlons()
                lats_2, lons_2 = grb_2.latlons()
                lats_3, lons_3 = grb_3.latlons()
                lats_4, lons_4 = grb_4.latlons()
                lats_5, lons_5 = grb_5.latlons()
                lats_6, lons_6 = None, None
                lats_7, lons_7 = None, None
                lats_8, lons_8 = None, None
    
            if count == 6: 
                grb_1 = GRIB_File_List[1]
                grb_2 = GRIB_File_List[2]
                grb_3 = GRIB_File_List[3]
                grb_4 = GRIB_File_List[4]
                grb_5 = GRIB_File_List[5]
                grb_6 = GRIB_File_List[6]
                grb_7 = None
                grb_8 = None
    
                grb_1_vals = grb_1.values
                grb_1_start = grb_1.validDate
                grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                grb_2_vals = grb_2.values
                grb_2_start = grb_2.validDate
                grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                grb_3_vals = grb_3.values
                grb_3_start = grb_3.validDate
                grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                grb_4_vals = grb_4.values
                grb_4_start = grb_4.validDate
                grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
                grb_5_vals = grb_5.values
                grb_5_start = grb_5.validDate
                grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
                grb_6_vals = grb_6.values
                grb_6_start = grb_6.validDate
                grb_6_end = grb_6_start + timedelta(hours=grid_time_interval)
                grb_7_vals = None
                grb_7_start = None
                grb_7_end = None
                grb_8_vals = None
                grb_8_start = None
                grb_8_end = None
    
                lats_1, lons_1 = grb_1.latlons()
                lats_2, lons_2 = grb_2.latlons()
                lats_3, lons_3 = grb_3.latlons()
                lats_4, lons_4 = grb_4.latlons()
                lats_5, lons_5 = grb_5.latlons()
                lats_6, lons_6 = grb_6.latlons()
                lats_7, lons_7 = None, None
                lats_8, lons_8 = None, None
    
            if count == 7: 
                grb_1 = GRIB_File_List[1]
                grb_2 = GRIB_File_List[2]
                grb_3 = GRIB_File_List[3]
                grb_4 = GRIB_File_List[4]
                grb_5 = GRIB_File_List[5]
                grb_6 = GRIB_File_List[6]
                grb_7 = GRIB_File_List[7]
                grb_8 = None

                grb_1_vals = grb_1.values
                grb_1_start = grb_1.validDate
                grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                grb_2_vals = grb_2.values
                grb_2_start = grb_2.validDate
                grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                grb_3_vals = grb_3.values
                grb_3_start = grb_3.validDate
                grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                grb_4_vals = grb_4.values
                grb_4_start = grb_4.validDate
                grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
                grb_5_vals = grb_5.values
                grb_5_start = grb_5.validDate
                grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
                grb_6_vals = grb_6.values
                grb_6_start = grb_6.validDate
                grb_6_end = grb_6_start + timedelta(hours=grid_time_interval)
                grb_7_vals = grb_7.values
                grb_7_start = grb_7.validDate
                grb_7_end = grb_7_start + timedelta(hours=grid_time_interval)
                grb_8_vals = None
                grb_8_start = None
                grb_8_end = None
    
                lats_1, lons_1 = grb_1.latlons()
                lats_2, lons_2 = grb_2.latlons()
                lats_3, lons_3 = grb_3.latlons()
                lats_4, lons_4 = grb_4.latlons()
                lats_5, lons_5 = grb_5.latlons()
                lats_6, lons_6 = grb_6.latlons()
                lats_7, lons_7 = grb_7.latlons()
                lats_8, lons_8 = None, None
    
            if count == 8: 
                grb_1 = GRIB_File_List[1]
                grb_2 = GRIB_File_List[2]
                grb_3 = GRIB_File_List[3]
                grb_4 = GRIB_File_List[4]
                grb_5 = GRIB_File_List[5]
                grb_6 = GRIB_File_List[6]
                grb_7 = GRIB_File_List[7]
                grb_8 = GRIB_File_List[8]

                grb_1_vals = grb_1.values
                grb_1_start = grb_1.validDate
                grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                grb_2_vals = grb_2.values
                grb_2_start = grb_2.validDate
                grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                grb_3_vals = grb_3.values
                grb_3_start = grb_3.validDate
                grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                grb_4_vals = grb_4.values
                grb_4_start = grb_4.validDate
                grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
                grb_5_vals = grb_5.values
                grb_5_start = grb_5.validDate
                grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
                grb_6_vals = grb_6.values
                grb_6_start = grb_6.validDate
                grb_6_end = grb_6_start + timedelta(hours=grid_time_interval)
                grb_7_vals = grb_7.values
                grb_7_start = grb_7.validDate
                grb_7_end = grb_7_start + timedelta(hours=grid_time_interval)
                grb_8_vals = grb_8.values
                grb_8_start = grb_8.validDate
                grb_8_end = grb_8_start + timedelta(hours=grid_time_interval)
    
                lats_1, lons_1 = grb_1.latlons()
                lats_2, lons_2 = grb_2.latlons()
                lats_3, lons_3 = grb_3.latlons()
                lats_4, lons_4 = grb_4.latlons()
                lats_5, lons_5 = grb_5.latlons()
                lats_6, lons_6 = grb_6.latlons()
                lats_7, lons_7 = grb_7.latlons()
                lats_8, lons_8 = grb_8.latlons()


            forecast_hour = grb_1_start.hour
    
            if file_path == 'ds.maxrh.bin':
                if forecast_hour == 6:
                    print("The " +file_path+ " forecast period begins at " + grb_1_start.strftime('%m/%d/%Y %HZ'))
                    print("\nThere are " + str(count) + " files returned.")
                    print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                    discard = False
                    
                    return grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard
                    
                else:
                    if local_hour < 4 or local_hour >= 16:
                        print("The " +file_path+ " forecast period began at " + grb_1_start.strftime('%m/%d/%Y %HZ') + "\nThe current time of " +local.strftime('%m/%d/%Y %H:00 Local')+ " is before 04:00 (4AM)\nThe first maximum temperature grid is still returned.")
    
                        year = utc.year
                        month = utc.month
                        day = utc.day
                        start_hour = 6
    
                        grb_1_start = datetime(year, month, day, start_hour)
                        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                        print("\nThere are " + str(count) + " files returned.")
                        print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                        discard = False
                        
                        return grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard
                        
                    else:
                        print("The first forecast grid from " + grb_1_start.strftime('%m/%d/%Y %HZ') + " is old and not valid anymore. The second forecast grid starting at " +grb_2_start.strftime('%m/%d/%Y %HZ') + " is the first forecast grid returned in this dataset.")

                        
                        discard = True
                        
                        try:
                            if grb_8_vals.all() != None:
                                test_8 = True
                
                        except Exception as e:
                            test_8 = False                        

                        if test_8 == False:
                            grb_8_vals = None
                            grb_8_start = None
                            grb_8_end = None
                            lats_8, lons_8 = None, None
                            count_of_GRIB_files = count - 1
                            count_short = count_short - 1
                            print("There is no 8th GRIB file.")
                            print("\nThere are " + str(count_of_GRIB_files) + " files returned.")
                            print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                            
                            return grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, grb_8_vals, grb_8_start, grb_8_end, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, lats_8, lons_8, count_of_GRIB_files, count_short, count_extended, discard

                        if test_8 == True:
                            print("There is an 8th GRIB file.")
                            count = count - 1
                            count_short = count_short - 1
                            print("\nThere are " + str(count) + " files returned.")
                            print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                            return grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, grb_8_vals, grb_8_start, grb_8_end, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, lats_8, lons_8, count, count_short, count_extended, discard


            if file_path == 'ds.minrh.bin':
                if forecast_hour == 18:
                    print("The " +file_path+ " forecast period begins at " + grb_1_start.strftime('%m/%d/%Y %HZ'))
                    print("\nThere are " + str(count) + " files returned.")
                    print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                    discard = False
                    
                    return grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard
                    
                else:
                    if local_hour < 14:
                        print("The " +file_path+ " forecast period began at " + grb_1_start.strftime('%m/%d/%Y %HZ') + "\nThe current time of " +local.strftime('%m/%d/%Y %H:00 Local')+ " is before 15:00 (3PM)\nThe first maximum temperature grid is still returned.")
    
                        year = utc.year
                        month = utc.month
                        day = utc.day
                        start_hour = 18

                        grb_1_start = datetime(year, month, day, start_hour)
                        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                        print("\nThere are " + str(count) + " files returned.")
                        print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                        discard = False
                        
                        return grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard
                        
                    else:
                        print("The first forecast grid from " + grb_1_start.strftime('%m/%d/%Y %HZ') + " is old and not valid anymore. The second forecast grid starting at " +grb_2_start.strftime('%m/%d/%Y %HZ') + " is the first forecast grid returned in this dataset.")

                        discard = True

                        try:
                            if grb_8_vals.all() != None:
                                test_8 = True
                
                        except Exception as e:
                            test_8 = False                        

                        if test_8 == False:
                            grb_8_vals = None
                            grb_8_start = None
                            grb_8_end = None
                            lats_8, lons_8 = None, None
                            count_of_GRIB_files = count - 1
                            count_short = count_short - 1
                            print("There is no 8th GRIB file.")
                            print("\nThere are " + str(count_of_GRIB_files) + " files returned.")
                            print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                            
                            return grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, grb_8_vals, grb_8_start, grb_8_end, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, lats_8, lons_8, count_of_GRIB_files, count_short, count_extended, discard

                        if test_8 == True:
                            print("There is an 8th GRIB file.")
                            count = count - 1
                            count_short = count_short - 1
                            print("\nThere are " + str(count) + " files returned.")
                            print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                            return grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, grb_8_vals, grb_8_start, grb_8_end, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, lats_8, lons_8, count, count_short, count_extended, discard


            if file_path == 'ds.critfireo.bin':
                if forecast_hour == 12:
                    print("The " +file_path+ " forecast period begins at " + grb_1_start.strftime('%m/%d/%Y %HZ'))
                    print("\nThere are " + str(count) + " files returned.")
                    print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                    discard = False
                    
                    return grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard
                    
                else:
                    if local_hour < 13:
                        print("The " +file_path+ " forecast period began at " + grb_1_start.strftime('%m/%d/%Y %HZ') + "\nThe current time of " +local.strftime('%m/%d/%Y %H:00 Local')+ " is before 13:00 (1PM)\nThe first maximum temperature grid is still returned.")
    
                        year = utc.year
                        month = utc.month
                        day = utc.day
                        start_hour = 12
                        discard = False
                        day_1 = grb_1_start.day
                        day_2 = grb_2_start.day
                        if day_1 == day_2:
                            print("Either duplicate or old files are being dowloaded.\nThrowing out the old file!")
                            discard = True
                            try:
                                if grb_8_vals.all() != None:
                                    test_8 = True
                    
                            except Exception as e:
                                test_8 = False    

                            if test_8 == False:
                                grb_8_vals = None
                                grb_8_start = None
                                grb_8_end = None
                                lats_8, lons_8 = None, None
                                count_of_GRIB_files = count - 2
                                print("There are " + str(count_of_GRIB_files) + " files returned.")
                                print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                                
                                return grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, grb_8_vals, grb_8_start, grb_8_end, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, lats_8, lons_8, count, count_short, count_extended, discard

                            if test_8 == True:
                                count_of_GRIB_files = count - 1
                                print("There are " + str(count_of_GRIB_files) + " files returned.")
                                print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                                
                                return grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, grb_8_vals, grb_8_start, grb_8_end, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, lats_8, lons_8, count, count_short, count_extended, discard
    
                        else:                   
                            grb_1_start = datetime(year, month, day, start_hour)
                            grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                            print("\nThere are " + str(count) + " files returned.")
                            print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                            
                            return grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard
                        
                    else:
                        print("The first forecast grid from " + grb_1_start.strftime('%m/%d/%Y %HZ') + " is old and not valid anymore. The second forecast grid starting at " +grb_2_start.strftime('%m/%d/%Y %HZ') + " is the first forecast grid returned in this dataset.")

                        discard = True

                        try:
                            if grb_8_vals.all() != None:
                                test_8 = True
                
                        except Exception as e:
                            test_8 = False                        

                        if test_8 == False:
                            grb_8_vals = None
                            grb_8_start = None
                            grb_8_end = None
                            count_of_GRIB_files = count - 1
                            count_short = count_short - 1
                            print("There is no 8th GRIB file.")
                            print("\nThere are " + str(count_of_GRIB_files) + " files returned.")
                            print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                            
                            return grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, grb_8_vals, grb_8_start, grb_8_end, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, lats_8, lons_8, count_of_GRIB_files, count_short, count_extended, discard

                        if test_8 == True:
                            print("There is an 8th GRIB file.")
                            count_short = count_short - 1
                            print("\nThere are " + str(count) + " files returned.")
                            print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")

                            return grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, grb_8_vals, grb_8_start, grb_8_end, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, lats_8, lons_8, count, count_short, count_extended, discard

            if file_path == 'ds.dryfireo.bin':
                if forecast_hour == 12:
                    print("The " +file_path+ " forecast period begins at " + grb_1_start.strftime('%m/%d/%Y %HZ'))
                    print("\nThere are " + str(count) + " files returned.")
                    print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                    discard = False
                    
                    return grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard
                    
                else:
                    if local_hour < 13:
                        print("The " +file_path+ " forecast period began at " + grb_1_start.strftime('%m/%d/%Y %HZ') + "\nThe current time of " +local.strftime('%m/%d/%Y %H:00 Local')+ " is before 13:00 (1PM)\nThe first maximum temperature grid is still returned.")
    
                        year = utc.year
                        month = utc.month
                        day = utc.day
                        start_hour = 12
                        discard = False
    
                        day_1 = grb_1_start.day
                        day_2 = grb_2_start.day
                        if day_1 == day_2:
                            print("Either duplicate or old files are being dowloaded.\nThrowing out the old file!")

                            discard = True
                            
                            try:
                                if grb_8_vals.all() != None:
                                    test_8 = True
                    
                            except Exception as e:
                                test_8 = False    

                            if test_8 == False:
                                grb_8_vals = None
                                grb_8_start = None
                                grb_8_end = None
                                lats_8, lons_8 = None, None
                                count_of_GRIB_files = count - 2
                                count_short = count_short - 1
                                print("There are " + str(count_of_GRIB_files) + " files returned.")
                                print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                                
                                return grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, grb_8_vals, grb_8_start, grb_8_end, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, lats_8, lons_8, count, count_short, count_extended, discard

                            if test_8 == True:
                                count_of_GRIB_files = count - 1
                                print("There are " + str(count_of_GRIB_files) + " files returned.")
                                print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                                
                                return grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, grb_8_vals, grb_8_start, grb_8_end, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, lats_8, lons_8, count, count_short, count_extended, discard
    
                        else:                 
                            grb_1_start = datetime(year, month, day, start_hour)
                            grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                            print("\nThere are " + str(count) + " files returned.")
                            print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                            
                            return grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard
                        
                    else:
                        print("The first forecast grid from " + grb_1_start.strftime('%m/%d/%Y %HZ') + " is old and not valid anymore. The second forecast grid starting at " +grb_2_start.strftime('%m/%d/%Y %HZ') + " is the first forecast grid returned in this dataset.")

                        discard = True

                        try:
                            if grb_8_vals.all() != None:
                                test_8 = True
                
                        except Exception as e:
                            test_8 = False                        

                        if test_8 == False:
                            grb_8_vals = None
                            grb_8_start = None
                            grb_8_end = None
                            lats_8, lons_8 = None, None
                            count_of_GRIB_files = count - 1
                            count_short = count_short - 1
                            print("There is no 8th GRIB file.")
                            print("\nThere are " + str(count_of_GRIB_files) + " files returned.")
                            print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                            
                            return grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, grb_8_vals, grb_8_start, grb_8_end, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, lats_8, lons_8, count_of_GRIB_files, count_short, count_extended, discard

                        if test_8 == True:
                            print("There is an 8th GRIB file.")
                            count_short = count_short - 1
                            print("\nThere are " + str(count) + " files returned.")
                            print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")

                            return grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, grb_8_vals, grb_8_start, grb_8_end, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, lats_8, lons_8, count, count_short, count_extended, discard

        if file_path == 'ds.mint.bin' or file_path == 'ds.maxt.bin':

            if convert_temperature == True:

                if count == 5: 
                    grb_1 = GRIB_File_List[1]
                    grb_2 = GRIB_File_List[2]
                    grb_3 = GRIB_File_List[3]
                    grb_4 = GRIB_File_List[4]
                    grb_5 = GRIB_File_List[5]
                    grb_6 = None
                    grb_7 = None
                    grb_8 = None
    
                    grb_1_start = grb_1.validDate
                    grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                    grb_2_start = grb_2.validDate
                    grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                    grb_3_start = grb_3.validDate
                    grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                    grb_4_start = grb_4.validDate
                    grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
                    grb_5_start = grb_5.validDate
                    grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
                    grb_6_start = None
                    grb_6_end = None
                    grb_7_start = None
                    grb_7_end = None
                    grb_8_start = None
                    grb_8_end = None
                    
                              
                    lats_1, lons_1 = grb_1.latlons()
                    lats_2, lons_2 = grb_2.latlons()
                    lats_3, lons_3 = grb_3.latlons()
                    lats_4, lons_4 = grb_4.latlons()
                    lats_5, lons_5 = grb_5.latlons()
                    lats_6, lons_6 = None, None
                    lats_7, lons_7 = None, None
                    lats_8, lons_8 = None, None
    
                if count == 6: 
                    grb_1 = GRIB_File_List[1]
                    grb_2 = GRIB_File_List[2]
                    grb_3 = GRIB_File_List[3]
                    grb_4 = GRIB_File_List[4]
                    grb_5 = GRIB_File_List[5]
                    grb_6 = GRIB_File_List[6]
                    grb_7 = None
                    grb_8 = None
    
                    grb_1 = GRIB_File_List[1]
                    grb_2 = GRIB_File_List[2]
                    grb_3 = GRIB_File_List[3]
                    grb_4 = GRIB_File_List[4]
                    grb_5 = GRIB_File_List[5]
                    grb_6 = GRIB_File_List[6]
                    grb_7 = None
                    grb_8 = None
        
                    grb_1_start = grb_1.validDate
                    grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                    grb_2_start = grb_2.validDate
                    grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                    grb_3_start = grb_3.validDate
                    grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                    grb_4_start = grb_4.validDate
                    grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
                    grb_5_start = grb_5.validDate
                    grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
                    grb_6_start = grb_6.validDate
                    grb_6_end = grb_6_start + timedelta(hours=grid_time_interval)
                    grb_7_start = None
                    grb_7_end = None
                    grb_8_start = None
                    grb_8_end = None
        
                    lats_1, lons_1 = grb_1.latlons()
                    lats_2, lons_2 = grb_2.latlons()
                    lats_3, lons_3 = grb_3.latlons()
                    lats_4, lons_4 = grb_4.latlons()
                    lats_5, lons_5 = grb_5.latlons()
                    lats_6, lons_6 = grb_6.latlons()
                    lats_7, lons_7 = None, None
                    lats_8, lons_8 = None, None
    
                if count == 7: 
                    grb_1 = GRIB_File_List[1]
                    grb_2 = GRIB_File_List[2]
                    grb_3 = GRIB_File_List[3]
                    grb_4 = GRIB_File_List[4]
                    grb_5 = GRIB_File_List[5]
                    grb_6 = GRIB_File_List[6]
                    grb_7 = GRIB_File_List[7]
                    grb_8 = None
    
                    grb_1_start = grb_1.validDate
                    grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                    grb_2_start = grb_2.validDate
                    grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                    grb_3_start = grb_3.validDate
                    grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                    grb_4_start = grb_4.validDate
                    grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
                    grb_5_start = grb_5.validDate
                    grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
                    grb_6_start = grb_6.validDate
                    grb_6_end = grb_6_start + timedelta(hours=grid_time_interval)
                    grb_7_start = grb_7.validDate
                    grb_7_end = grb_7_start + timedelta(hours=grid_time_interval)
                    grb_8_start = None
                    grb_8_end = None
        
                    lats_1, lons_1 = grb_1.latlons()
                    lats_2, lons_2 = grb_2.latlons()
                    lats_3, lons_3 = grb_3.latlons()
                    lats_4, lons_4 = grb_4.latlons()
                    lats_5, lons_5 = grb_5.latlons()
                    lats_6, lons_6 = grb_6.latlons()
                    lats_7, lons_7 = grb_7.latlons()
                    lats_8, lons_8 = None, None
    
                if count == 8: 
                    grb_1 = GRIB_File_List[1]
                    grb_2 = GRIB_File_List[2]
                    grb_3 = GRIB_File_List[3]
                    grb_4 = GRIB_File_List[4]
                    grb_5 = GRIB_File_List[5]
                    grb_6 = GRIB_File_List[6]
                    grb_7 = GRIB_File_List[7]
                    grb_8 = GRIB_File_List[8]
    
                    grb_1_start = grb_1.validDate
                    grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                    grb_2_start = grb_2.validDate
                    grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                    grb_3_start = grb_3.validDate
                    grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                    grb_4_start = grb_4.validDate
                    grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
                    grb_5_start = grb_5.validDate
                    grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
                    grb_6_start = grb_6.validDate
                    grb_6_end = grb_6_start + timedelta(hours=grid_time_interval)
                    grb_7_start = grb_7.validDate
                    grb_7_end = grb_7_start + timedelta(hours=grid_time_interval)
                    grb_8_start = grb_8.validDate
                    grb_8_end = grb_8_start + timedelta(hours=grid_time_interval)
        
                    lats_1, lons_1 = grb_1.latlons()
                    lats_2, lons_2 = grb_2.latlons()
                    lats_3, lons_3 = grb_3.latlons()
                    lats_4, lons_4 = grb_4.latlons()
                    lats_5, lons_5 = grb_5.latlons()
                    lats_6, lons_6 = grb_6.latlons()
                    lats_7, lons_7 = grb_7.latlons()
                    lats_8, lons_8 = grb_8.latlons()
    
                
                grb_1_vals, grb_2_vals, grb_3_vals, grb_4_vals, grb_5_vals, grb_6_vals, grb_7_vals, grb_8_vals = NDFD.GRIB_temperature_conversion_7_day(grb_1, grb_2, grb_3, grb_4, grb_5, grb_6, grb_7, grb_8, count)

            else:

                if count == 5: 
                    grb_1 = GRIB_File_List[1]
                    grb_2 = GRIB_File_List[2]
                    grb_3 = GRIB_File_List[3]
                    grb_4 = GRIB_File_List[4]
                    grb_5 = GRIB_File_List[5]
                    grb_6 = None
                    grb_7 = None
                    grb_8 = None
        
                    grb_1_vals = grb_1.values
                    grb_1_start = grb_1.validDate
                    grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                    grb_2_vals = grb_2.values
                    grb_2_start = grb_2.validDate
                    grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                    grb_3_vals = grb_3.values
                    grb_3_start = grb_3.validDate
                    grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                    grb_4_vals = grb_4.values
                    grb_4_start = grb_4.validDate
                    grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
                    grb_5_vals = grb_5.values
                    grb_5_start = grb_5.validDate
                    grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
                    grb_6_vals = None
                    grb_6_start = None
                    grb_6_end = None
                    grb_7_vals = None
                    grb_7_start = None
                    grb_7_end = None
                    grb_8_vals = None
                    grb_8_start = None
                    grb_8_end = None
                    
                              
                    lats_1, lons_1 = grb_1.latlons()
                    lats_2, lons_2 = grb_2.latlons()
                    lats_3, lons_3 = grb_3.latlons()
                    lats_4, lons_4 = grb_4.latlons()
                    lats_5, lons_5 = grb_5.latlons()
                    lats_6, lons_6 = None, None
                    lats_7, lons_7 = None, None
                    lats_8, lons_8 = None, None
        
                if count == 6: 
                    grb_1 = GRIB_File_List[1]
                    grb_2 = GRIB_File_List[2]
                    grb_3 = GRIB_File_List[3]
                    grb_4 = GRIB_File_List[4]
                    grb_5 = GRIB_File_List[5]
                    grb_6 = GRIB_File_List[6]
                    grb_7 = None
                    grb_8 = None
        
                    grb_1_vals = grb_1.values
                    grb_1_start = grb_1.validDate
                    grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                    grb_2_vals = grb_2.values
                    grb_2_start = grb_2.validDate
                    grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                    grb_3_vals = grb_3.values
                    grb_3_start = grb_3.validDate
                    grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                    grb_4_vals = grb_4.values
                    grb_4_start = grb_4.validDate
                    grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
                    grb_5_vals = grb_5.values
                    grb_5_start = grb_5.validDate
                    grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
                    grb_6_vals = grb_6.values
                    grb_6_start = grb_6.validDate
                    grb_6_end = grb_6_start + timedelta(hours=grid_time_interval)
                    grb_7_vals = None
                    grb_7_start = None
                    grb_7_end = None
                    grb_8_vals = None
                    grb_8_start = None
                    grb_8_end = None
        
                    lats_1, lons_1 = grb_1.latlons()
                    lats_2, lons_2 = grb_2.latlons()
                    lats_3, lons_3 = grb_3.latlons()
                    lats_4, lons_4 = grb_4.latlons()
                    lats_5, lons_5 = grb_5.latlons()
                    lats_6, lons_6 = grb_6.latlons()
                    lats_7, lons_7 = None, None
                    lats_8, lons_8 = None, None
        
                if count == 7: 
                    grb_1 = GRIB_File_List[1]
                    grb_2 = GRIB_File_List[2]
                    grb_3 = GRIB_File_List[3]
                    grb_4 = GRIB_File_List[4]
                    grb_5 = GRIB_File_List[5]
                    grb_6 = GRIB_File_List[6]
                    grb_7 = GRIB_File_List[7]
                    grb_8 = None
        
                    grb_1_vals = grb_1.values
                    grb_1_start = grb_1.validDate
                    grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                    grb_2_vals = grb_2.values
                    grb_2_start = grb_2.validDate
                    grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                    grb_3_vals = grb_3.values
                    grb_3_start = grb_3.validDate
                    grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                    grb_4_vals = grb_4.values
                    grb_4_start = grb_4.validDate
                    grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
                    grb_5_vals = grb_5.values
                    grb_5_start = grb_5.validDate
                    grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
                    grb_6_vals = grb_6.values
                    grb_6_start = grb_6.validDate
                    grb_6_end = grb_6_start + timedelta(hours=grid_time_interval)
                    grb_7_vals = grb_7.values
                    grb_7_start = grb_7.validDate
                    grb_7_end = grb_7_start + timedelta(hours=grid_time_interval)
                    grb_8_vals = None
                    grb_8_start = None
                    grb_8_end = None
        
                    lats_1, lons_1 = grb_1.latlons()
                    lats_2, lons_2 = grb_2.latlons()
                    lats_3, lons_3 = grb_3.latlons()
                    lats_4, lons_4 = grb_4.latlons()
                    lats_5, lons_5 = grb_5.latlons()
                    lats_6, lons_6 = grb_6.latlons()
                    lats_7, lons_7 = grb_7.latlons()
                    lats_8, lons_8 = None, None
        
                if count == 8: 
                    grb_1 = GRIB_File_List[1]
                    grb_2 = GRIB_File_List[2]
                    grb_3 = GRIB_File_List[3]
                    grb_4 = GRIB_File_List[4]
                    grb_5 = GRIB_File_List[5]
                    grb_6 = GRIB_File_List[6]
                    grb_7 = GRIB_File_List[7]
                    grb_8 = GRIB_File_List[8]
        
                    grb_1_vals = grb_1.values
                    grb_1_start = grb_1.validDate
                    grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                    grb_2_vals = grb_2.values
                    grb_2_start = grb_2.validDate
                    grb_2_end = grb_2_start + timedelta(hours=grid_time_interval)
                    grb_3_vals = grb_3.values
                    grb_3_start = grb_3.validDate
                    grb_3_end = grb_3_start + timedelta(hours=grid_time_interval)
                    grb_4_vals = grb_4.values
                    grb_4_start = grb_4.validDate
                    grb_4_end = grb_4_start + timedelta(hours=grid_time_interval)
                    grb_5_vals = grb_5.values
                    grb_5_start = grb_5.validDate
                    grb_5_end = grb_5_start + timedelta(hours=grid_time_interval)
                    grb_6_vals = grb_6.values
                    grb_6_start = grb_6.validDate
                    grb_6_end = grb_6_start + timedelta(hours=grid_time_interval)
                    grb_7_vals = grb_7.values
                    grb_7_start = grb_7.validDate
                    grb_7_end = grb_7_start + timedelta(hours=grid_time_interval)
                    grb_8_vals = grb_8.values
                    grb_8_start = grb_8.validDate
                    grb_8_end = grb_8_start + timedelta(hours=grid_time_interval)
        
                    lats_1, lons_1 = grb_1.latlons()
                    lats_2, lons_2 = grb_2.latlons()
                    lats_3, lons_3 = grb_3.latlons()
                    lats_4, lons_4 = grb_4.latlons()
                    lats_5, lons_5 = grb_5.latlons()
                    lats_6, lons_6 = grb_6.latlons()
                    lats_7, lons_7 = grb_7.latlons()
                    lats_8, lons_8 = grb_8.latlons()

            forecast_hour = grb_1_start.hour

            if file_path == 'ds.mint.bin':
                if forecast_hour == 0:
                    print("The " +file_path+ " forecast period begins at " + grb_1_start.strftime('%m/%d/%Y %HZ'))
                    print("\nThere are " + str(count) + " files returned.")
                    print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                    discard = False
                    
                    return grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard
                    
                else:
                    if local_hour < 4 or local_hour >= 16:
                        print("The " +file_path+ " forecast period began at " + grb_1_start.strftime('%m/%d/%Y %HZ') + "\nThe current time of " +local.strftime('%m/%d/%Y %H:00 Local')+ " is before 04:00 (4AM)\nThe first maximum temperature grid is still returned.")
    
                        year = utc.year
                        month = utc.month
                        day = utc.day
                        start_hour = 0
    
                        grb_1_start = datetime(year, month, day, start_hour)
                        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                        print("\nThere are " + str(count) + " files returned.")
                        print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                        discard = False
                        
                        return grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard
                        
                    else:
                        print("The first forecast grid from " + grb_1_start.strftime('%m/%d/%Y %HZ') + " is old and not valid anymore. The second forecast grid starting at " +grb_2_start.strftime('%m/%d/%Y %HZ') + " is the first forecast grid returned in this dataset.")

                        discard = True
                        

                        try:
                            if grb_8_vals.all() != None:
                                test_8 = True
                
                        except Exception as e:
                            test_8 = False                        

                        if test_8 == False:
                            grb_8_vals = None
                            grb_8_start = None
                            grb_8_end = None
                            lats_8, lons_8 = None, None
                            count_of_GRIB_files = count - 1
                            count_short = count_short - 1
                            print("There is no 8th GRIB file.")
                            print("\nThere are " + str(count_of_GRIB_files) + " files returned.")
                            print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                            
                            return grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, grb_8_vals, grb_8_start, grb_8_end, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, lats_8, lons_8, count_of_GRIB_files, count_short, count_extended, discard

                        if test_8 == True:
                            print("There is an 8th GRIB file.")
                            count = count - 1
                            count_short = count_short - 1
                            print("\nThere are " + str(count) + " files returned.")
                            print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                            
                            return grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, grb_8_vals, grb_8_start, grb_8_end, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, lats_8, lons_8, count, count_short, count_extended, discard


            if file_path == 'ds.maxt.bin':
                if forecast_hour == 12:
                    print("The " +file_path+ " forecast period begins at " + grb_1_start.strftime('%m/%d/%Y %HZ'))
                    print("\nThere are " + str(count) + " files returned.")
                    print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                    discard = False
                    
                    return grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard
                    
                else:
                    if local_hour < 14 or local_hour >= 18:
                        print("The " +file_path+ " forecast period began at " + grb_1_start.strftime('%m/%d/%Y %HZ') + "\nThe current time of " +local.strftime('%m/%d/%Y %H:00 Local')+ " is before 15:00 (3PM)\nThe first maximum temperature grid is still returned.")
    
                        year = utc.year
                        month = utc.month
                        day = utc.day
                        start_hour = 12
    
                        grb_1_start = datetime(year, month, day, start_hour)
                        grb_1_end = grb_1_start + timedelta(hours=grid_time_interval)
                        print("\nThere are " + str(count) + " files returned.")
                        print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                        discard = False
                        
                        return grb_1_vals, grb_1_start, grb_1_end, grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, lats_1, lons_1, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, count, count_short, count_extended, discard
                        
                    else:
                        print("The first forecast grid from " + grb_1_start.strftime('%m/%d/%Y %HZ') + " is old and not valid anymore. The second forecast grid starting at " +grb_2_start.strftime('%m/%d/%Y %HZ') + " is the first forecast grid returned in this dataset.")

                        discard = True

                        try:
                            if grb_8_vals.all() != None:
                                test_8 = True
                
                        except Exception as e:
                            test_8 = False                        

                        if test_8 == False:
                            grb_8_vals = None
                            grb_8_start = None
                            grb_8_end = None
                            lats_8, lons_8 = None, None
                            count_of_GRIB_files = count - 1
                            count_short = count_short - 1
                            print("There is no 8th GRIB file.")
                            print("\nThere are " + str(count_of_GRIB_files) + " files returned.")
                            print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                            
                            return grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, grb_8_vals, grb_8_start, grb_8_end, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, lats_8, lons_8, count_of_GRIB_files, count_short, count_extended, discard

                        if test_8 == True:
                            print("There is an 8th GRIB file.")
                            count = count - 1
                            count_short = count_short - 1
                            print("\nThere are " + str(count) + " files returned.")
                            print("\n"+str(count_short)+" short-term files.\n"+str(count_extended)+" extended files.")
                            
                            return grb_2_vals, grb_2_start, grb_2_end, grb_3_vals, grb_3_start, grb_3_end, grb_4_vals, grb_4_start, grb_4_end, grb_5_vals, grb_5_start, grb_5_end, grb_6_vals, grb_6_start, grb_6_end, grb_7_vals, grb_7_start, grb_7_end, grb_8_vals, grb_8_start, grb_8_end, lats_2, lons_2, lats_3, lons_3, lats_4, lons_4, lats_5, lons_5, lats_6, lons_6, lats_7, lons_7, lats_8, lons_8, count, count_short, count_extended, discard


class checks:

    r'''

    THIS CLASS HOSTS FUNCTIONS TO CHECK TO MAKE SURE WE ARE COMPARING DATASETS FOR THE SAME TIME

    '''

    def wind_direction_number_to_abbreviation(wind_direction):

        r'''
        This function takes the numerical wind direction and assigns an abbreviation (i.e. N vs. NW) to the value

        Inputs:
                1) wind_direction (Integer or Float)

        Returns:
                1) wind_direction (String)

        '''
        wind_direction = wind_direction
        
        if wind_direction >= 358 or wind_direction <= 2:
            wind_dir = 'N'
        if wind_direction > 2 and wind_direction <= 30:
            wind_dir = 'NNE'
        if wind_direction > 30 and wind_direction <= 60:
            wind_dir = 'NE'
        if wind_direction > 60 and wind_direction < 88:
            wind_dir = 'ENE'
        if wind_direction >= 88 and wind_direction <= 92:
            wind_dir = 'E'
        if wind_direction > 92 and wind_direction <= 120:
            wind_dir = 'ESE'
        if wind_direction > 120 and wind_direction <= 150:
            wind_dir = 'SE'
        if wind_direction > 150 and wind_direction < 178:
            wind_dir = 'SSE'
        if wind_direction >= 178 and wind_direction <= 182:
            wind_dir = 'S'
        if wind_direction > 182 and wind_direction <= 210:
            wind_dir = 'SSW'
        if wind_direction > 210 and wind_direction <= 240:
            wind_dir = 'SW'
        if wind_direction > 240 and wind_direction < 268:
            wind_dir = 'WSW'
        if wind_direction >= 268 and wind_direction <= 272:
            wind_dir = 'W'
        if wind_direction > 272 and wind_direction <= 300:
            wind_dir = 'WNW'
        if wind_direction > 300 and wind_direction <= 330:
            wind_dir = 'NW'
        if wind_direction > 330 and wind_direction < 358:
            wind_dir = 'NNW'

        return wind_dir
    

    def check_RTMA_vs_METAR_Times(real_time_mesoscale_analysis_time, metar_observation_time):

        r'''
        THIS FUNCTION MAKES SURE THE TIMES MATCH BETWEEN THE RTMA DATA AND METAR DATA. A LOT OF TIMES, THE METAR DATA IS 1-2 HOURS AHEAD OF THE RTMA DATA. THE FUNCTION RETURNS THE TIME OF THE LATEST RTMA DATASET TO USE AS THE TIME WHEN QUERYING THE METAR DATASETS

        (C) METEOROLOGIST ERIC J. DREWITZ

        '''

        metar_time = metar_observation_time

        rtma_time = real_time_mesoscale_analysis_time

        time_diff = metar_time.hour - rtma_time.hour

        if metar_time.hour > rtma_time.hour:
            new_metar_time = metar_time - timedelta(hours=time_diff)

        if metar_time.hour < rtma_time.hour:
            hour = rtma_time.hour
            new_metar_time = metar_time - timedelta(days=1)
            year = new_metar_time.year
            month = new_metar_time.month
            day = new_metar_time.day
            new_metar_time = datetime(year, month, day, hour)

        else:
            new_metar_time = rtma_time
            

        return new_metar_time


    def check_RTMA_vs_METAR_Times_Alaska(real_time_mesoscale_analysis_time, metar_observation_time):

        r'''
        THIS FUNCTION MAKES SURE THE TIMES MATCH BETWEEN THE RTMA DATA AND METAR DATA. A LOT OF TIMES, THE METAR DATA IS 1-2 HOURS AHEAD OF THE RTMA DATA. THE FUNCTION RETURNS THE TIME OF THE LATEST RTMA DATASET TO USE AS THE TIME WHEN QUERYING THE METAR DATASETS

        (C) METEOROLOGIST ERIC J. DREWITZ

        '''

        metar_time = metar_observation_time

        rtma_time = real_time_mesoscale_analysis_time

        time_diff = metar_time.hour - rtma_time.hour

        minute = 55

        if metar_time.hour > rtma_time.hour:
            new_metar_time = metar_time - timedelta(hours=2)
            new_metar_time1 = datetime(new_metar_time.year, new_metar_time.month, new_metar_time.day, new_metar_time.hour, minute)

        if metar_time.hour < rtma_time.hour:
            hour = rtma_time.hour
            new_metar_time = metar_time - timedelta(days=1)
            year = new_metar_time.year
            month = new_metar_time.month
            day = new_metar_time.day
            new_metar_time1 = datetime(year, month, day, hour, minute)

        else:
            new_metar_time = metar_time - timedelta(hours=1)
            new_metar_time1 = datetime(new_metar_time.year, new_metar_time.month, new_metar_time.day, new_metar_time.hour, minute)

        return new_metar_time1


    def parse_NWS_GRIB_data_array(data_array, parameter, file_count, convert_to_pandas_dataframe, count_short, count_extended, discard):


        ds = data_array
        parameter = parameter
        file_count = file_count
        count_short = count_short 
        count_extended = count_extended
        convert_to_pandas_dataframe = convert_to_pandas_dataframe
        discard = discard
        
        try:
            count = 0
            for i in data_array['time']:
                count = count + 1

        except Exception as e:
            count = 0

        vals = []
        if count == 2:
            try:
                if discard == False:
                    vals_00 = ds[parameter][1, 0, :, :]
                    vals_01 = ds[parameter][1, 1, :, :]
                    if count_short == 2:
                        vals_02 = ds[parameter][0, 2, :, :]
                        vals_03 = ds[parameter][0, 3, :, :]
                        vals_04 = ds[parameter][0, 4, :, :]                    
                    if count_short == 3:
                        vals_02 = ds[parameter][1, 2, :, :]
                        vals_03 = ds[parameter][0, 3, :, :]
                        vals_04 = ds[parameter][0, 4, :, :]
                    if count_short == 4:
                        vals_02 = ds[parameter][1, 2, :, :]
                        vals_03 = ds[parameter][1, 3, :, :]
                        vals_04 = ds[parameter][0, 4, :, :]
                    if count_short == 5:
                        vals_02 = ds[parameter][1, 2, :, :]
                        vals_03 = ds[parameter][1, 3, :, :]
                        vals_04 = ds[parameter][1, 4, :, :]
                    vals_05 = ds[parameter][0, 5, :, :]
                    if file_count >= 7:
                        vals_06 = ds[parameter][0, 6, :, :]
        
                if discard == True:
                    vals_00 = ds[parameter][1, 1, :, :]
                    vals_01 = ds[parameter][1, 2, :, :]
                    if count_short == 2:
                        vals_02 = ds[parameter][0, 3, :, :]
                        vals_03 = ds[parameter][0, 4, :, :]
                        vals_04 = ds[parameter][0, 5, :, :]                    
                    if count_short == 3:
                        vals_02 = ds[parameter][1, 3, :, :]
                        vals_03 = ds[parameter][0, 4, :, :]
                        vals_04 = ds[parameter][0, 5, :, :]
                    if count_short == 4:
                        vals_02 = ds[parameter][1, 3, :, :]
                        vals_03 = ds[parameter][1, 4, :, :]
                        vals_04 = ds[parameter][0, 5, :, :]
                    if count_short == 5:
                        vals_02 = ds[parameter][1, 3, :, :]
                        vals_03 = ds[parameter][1, 4, :, :]
                        vals_04 = ds[parameter][1, 5, :, :]
                    vals_05 = ds[parameter][0, 6, :, :]
                    if file_count >= 7:
                        vals_06 = ds[parameter][0, 7, :, :]

            except Exception as e:
                if discard == False:
                    vals_00 = ds[parameter][1, 0, :]
                    vals_01 = ds[parameter][1, 1, :]
                    if count_short == 2:
                        vals_02 = ds[parameter][0, 2, :]
                        vals_03 = ds[parameter][0, 3, :]
                        vals_04 = ds[parameter][0, 4, :]                    
                    if count_short == 3:
                        vals_02 = ds[parameter][1, 2, :]
                        vals_03 = ds[parameter][0, 3, :]
                        vals_04 = ds[parameter][0, 4, :]
                    if count_short == 4:
                        vals_02 = ds[parameter][1, 2, :]
                        vals_03 = ds[parameter][1, 3, :]
                        vals_04 = ds[parameter][0, 4, :]
                    if count_short == 5:
                        vals_02 = ds[parameter][1, 2, :]
                        vals_03 = ds[parameter][1, 3, :]
                        vals_04 = ds[parameter][1, 4, :]
                    vals_05 = ds[parameter][0, 5, :]
                    if file_count >= 7:
                        vals_06 = ds[parameter][0, 6, :]
        
                if discard == True:
                    vals_00 = ds[parameter][1, 1, :]
                    vals_01 = ds[parameter][1, 2, :]
                    if count_short == 2:
                        vals_02 = ds[parameter][0, 3, :]
                        vals_03 = ds[parameter][0, 4, :]
                        vals_04 = ds[parameter][0, 5, :]                    
                    if count_short == 3:
                        vals_02 = ds[parameter][1, 3, :]
                        vals_03 = ds[parameter][0, 4, :]
                        vals_04 = ds[parameter][0, 5, :]
                    if count_short == 4:
                        vals_02 = ds[parameter][1, 3, :]
                        vals_03 = ds[parameter][1, 4, :]
                        vals_04 = ds[parameter][0, 5, :]
                    if count_short == 5:
                        vals_02 = ds[parameter][1, 3, :]
                        vals_03 = ds[parameter][1, 4, :]
                        vals_04 = ds[parameter][1, 5, :]
                    vals_05 = ds[parameter][0, 6, :]
                    if file_count >= 7:
                        vals_06 = ds[parameter][0, 7, :]                

            vals.append(vals_00)
            vals.append(vals_01)
            vals.append(vals_02)
            vals.append(vals_03)
            vals.append(vals_04)
            vals.append(vals_05)
            if file_count >= 7:
                vals.append(vals_06)                
                if file_count == 8:
                    vals_07 = ds[parameter][0, 7, :, :]
                    vals.append(vals_07)
  

        if count == 1:
            if discard == False:
                vals_00 = ds[parameter][0, 0, :, :]
                vals_01 = ds[parameter][0, 1, :, :]
                vals_02 = ds[parameter][0, 2, :, :]
                vals_03 = ds[parameter][0, 3, :, :]
                vals_04 = ds[parameter][0, 4, :, :]
                vals_05 = ds[parameter][0, 5, :, :]
                if file_count >= 7:
                    vals_06 = ds[parameter][0, 6, :, :]
            if discard == True:
                vals_00 = ds[parameter][0, 1, :, :]
                vals_01 = ds[parameter][0, 2, :, :]
                vals_02 = ds[parameter][0, 3, :, :]
                vals_03 = ds[parameter][0, 4, :, :]
                vals_04 = ds[parameter][0, 5, :, :]
                vals_05 = ds[parameter][0, 6, :, :]
                if file_count >= 7:
                    vals_06 = ds[parameter][0, 7, :, :]

            vals.append(vals_00)
            vals.append(vals_01)
            vals.append(vals_02)
            vals.append(vals_03)
            vals.append(vals_04)
            vals.append(vals_05)
            if file_count >= 7:
                vals.append(vals_06)                
                if file_count == 8:
                    vals_07 = ds[parameter][0, 7, :, :]
                    vals.append(vals_07)
            

        if count == 0:
            if discard == False:
                vals_00 = ds[parameter][0, :, :]
                vals_01 = ds[parameter][1, :, :]
                vals_02 = ds[parameter][2, :, :]
                vals_03 = ds[parameter][3, :, :]
                vals_04 = ds[parameter][4, :, :]
                vals_05 = ds[parameter][5, :, :]
                if file_count >= 7:
                    vals_06 = ds[parameter][6, :, :]

            if discard == True:
                vals_00 = ds[parameter][1, :, :]
                vals_01 = ds[parameter][2, :, :]
                vals_02 = ds[parameter][3, :, :]
                vals_03 = ds[parameter][4, :, :]
                vals_04 = ds[parameter][5, :, :]
                vals_05 = ds[parameter][6, :, :]
                if file_count >= 7:
                    vals_06 = ds[parameter][7, :, :]


            vals.append(vals_00)
            vals.append(vals_01)
            vals.append(vals_02)
            vals.append(vals_03)
            vals.append(vals_04)
            vals.append(vals_05)
            if file_count >= 7:
                vals.append(vals_06)                
                if file_count == 8:
                    vals_07 = ds[parameter][7, :, :]
                    vals.append(vals_07)


        if convert_to_pandas_dataframe == False:
            return vals

        if convert_to_pandas_dataframe == True:
            vals_df = []
            ds0 = vals[0]
            ds1 = vals[1]
            ds2 = vals[2]
            ds3 = vals[3]
            ds4 = vals[4]
            ds5 = vals[5]
            if file_count >= 7:
                ds6 = vals[6]

            df0 = ds0.to_dataframe()
            df1 = ds1.to_dataframe()
            df2 = ds2.to_dataframe()
            df3 = ds3.to_dataframe()
            df4 = ds4.to_dataframe()
            df5 = ds5.to_dataframe()
            if file_count >= 7:
                df6 = ds6.to_dataframe()

            if file_count < 8:
                vals_df.append(df0)
            vals_df.append(df1)
            vals_df.append(df2)
            vals_df.append(df3)
            vals_df.append(df4)
            vals_df.append(df5)
            if file_count >= 7:
                vals_df.append(df6)
            
            if file_count == 8:
                ds7 = vals[7]
                df7 = ds7.to_dataframe()
                vals_df.append(df7)
   
            return vals_df



        
