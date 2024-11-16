# Importing needed packages
import urllib.request
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib as mpl
import firewxpy.standard as standard
import pytz

from datetime import datetime, timedelta

mpl.rcParams['font.weight'] = 'bold'

def sawti(zone_1_threshold_1=10, zone_1_threshold_2=15, zone_1_threshold_3=21, zone_1_threshold_4=40, zone_2_threshold_1=9, zone_2_threshold_2=13, zone_2_threshold_3=20, zone_2_threshold_4=28, zone_3_threshold_1=10, zone_3_threshold_2=16, zone_3_threshold_3=24, zone_3_threshold_4=36, zone_4_threshold_1=9, zone_4_threshold_2=12, zone_4_threshold_3=15, zone_4_threshold_4=25, zone_1_W_weight=1, zone_1_DD_weight=1, zone_1_FMC_weight=1, zone_2_W_weight=1, zone_2_DD_weight=1, zone_2_FMC_weight=1, zone_3_W_weight=1, zone_3_DD_weight=1, zone_3_FMC_weight=1, zone_4_W_weight=1, zone_4_DD_weight=1, zone_4_FMC_weight=1):

    r'''
    This function calculates the The Santa Ana Wildfire Threat Index from Rolinski et al. 2016. The function downloads the .CSV files holding the data, performs the Large Fire Potential (LFP) calculation and makes a bar graph
    for each zone. 

    Literature Citation: Rolinski, T., S. B. Capps, R. G. Fovell, Y. Cao, B. J. D’Agostino, and S. Vanderburg, 2016: The Santa Ana Wildfire Threat Index: Methodology and Operational Implementation. Wea. Forecasting, 31, 1881–1897, https://doi.org/10.1175/WAF-D-15-0141.1.

    Required Arguments: None

    Optional Arguments: 1) zone_1_threshold_1 (Integer) - Default = 10. This is the LFP threshold that seprates no rating (green zone) and a marginal risk (yellow zone) for zone 1. 
                        2) zone_1_threshold_2 (Integer) - Default = 15. This is the LFP threshold that seprates a marginal risk (yellow zone) and a moderate risk (orange zone) for zone 1. 
                        3) zone_1_threshold_3 (Integer) - Default = 21. This is the LFP threshold that seprates a moderate risk (orange zone) and a high risk (red zone) for zone 1. 
                        4) zone_1_threshold_4 (Integer) - Default = 40. This is the LFP threshold that seprates a high risk (red zone) and an extreme risk (purple zone) for zone 1. 
                        5) zone_2_threshold_1 (Integer) - Default = 9. This is the LFP threshold that seprates no rating (green zone) and a marginal risk (yellow zone) for zone 2. 
                        6) zone_2_threshold_2 (Integer) - Default = 13. This is the LFP threshold that seprates a marginal risk (yellow zone) and a moderate risk (orange zone) for zone 2. 
                        7) zone_2_threshold_3 (Integer) - Default = 20. This is the LFP threshold that seprates a moderate risk (orange zone) and a high risk (red zone) for zone 2. 
                        8) zone_2_threshold_4 (Integer) - Default = 28. This is the LFP threshold that seprates a high risk (red zone) and an extreme risk (purple zone) for zone 2. 
                        9) zone_3_threshold_1 (Integer) - Default = 10. This is the LFP threshold that seprates no rating (green zone) and a marginal risk (yellow zone) for zone 3. 
                        10) zone_3_threshold_2 (Integer) - Default = 16. This is the LFP threshold that seprates a marginal risk (yellow zone) and a moderate risk (orange zone) for zone 3. 
                        11) zone_3_threshold_3 (Integer) - Default = 24. This is the LFP threshold that seprates a moderate risk (orange zone) and a high risk (red zone) for zone 3. 
                        12) zone_3_threshold_4 (Integer) - Default = 36. This is the LFP threshold that seprates a high risk (red zone) and an extreme risk (purple zone) for zone 3. 
                        13) zone_4_threshold_1 (Integer) - Default = 9. This is the LFP threshold that seprates no rating (green zone) and a marginal risk (yellow zone) for zone 4. 
                        14) zone_4_threshold_2 (Integer) - Default = 12. This is the LFP threshold that seprates a marginal risk (yellow zone) and a moderate risk (orange zone) for zone 4. 
                        15) zone_4_threshold_3 (Integer) - Default = 15. This is the LFP threshold that seprates a moderate risk (orange zone) and a high risk (red zone) for zone 4. 
                        16) zone_4_threshold_4 (Integer) - Default = 25. This is the LFP threshold that seprates a high risk (red zone) and an extreme risk (purple zone) for zone 4.
                        17) zone_1_W_weight (Float or Integer) - Default = 1. This is the weight to multiply the wind-squared value by for zone 1. 
                        18) zone_1_DD_weight (Float or Integer) - Default = 1. This is the weight to multiply the dew point depression value by for zone 1. 
                        19) zone_1_FMC_weight (Float or Integer) - Default = 1. This is the weight to multiply the fuel moisture component value by for zone 1. 
                        20) zone_2_W_weight (Float or Integer) - Default = 1. This is the weight to multiply the wind-squared value by for zone 2. 
                        21) zone_2_DD_weight (Float or Integer) - Default = 1. This is the weight to multiply the dew point depression value by for zone 2. 
                        22) zone_2_FMC_weight (Float or Integer) - Default = 1. This is the weight to multiply the fuel moisture component value by for zone 2. 
                        23) zone_3_W_weight (Float or Integer) - Default = 1. This is the weight to multiply the wind-squared value by for zone 3. 
                        24) zone_3_DD_weight (Float or Integer) - Default = 1. This is the weight to multiply the dew point depression value by for zone 3. 
                        25) zone_3_FMC_weight (Float or Integer) - Default = 1. This is the weight to multiply the fuel moisture component value by for zone 3. 
                        26) zone_4_W_weight (Float or Integer) - Default = 1. This is the weight to multiply the wind-squared value by for zone 4. 
                        27) zone_4_DD_weight (Float or Integer) - Default = 1. This is the weight to multiply the dew point depression value by for zone 4. 
                        28) zone_4_FMC_weight (Float or Integer) - Default = 1. This is the weight to multiply the fuel moisture component value by for zone 4. 

    Returns: A graphic showing the LFP forecast for each zone saved to f:Weather Data/SAWTI. 
                        
    '''

    local_time, utc_time = standard.plot_creation_time()

    now = datetime.utcnow()
    yday = now - timedelta(days=1)
    day2 = now + timedelta(days=1)
    day3 = now + timedelta(days=2)
    day4 = now + timedelta(days=3)
    day5 = now + timedelta(days=4)
    day6 = now + timedelta(days=5)
    day7 = now + timedelta(days=6)
    
    # Zone 1

    if os.path.exists('seaspace_zone1_'+now.strftime('%m%d%Y')+'_12z.csv'):
        os.remove('seaspace_zone1_'+now.strftime('%m%d%Y')+'_12z.csv')
        print('seaspace_zone1_'+now.strftime('%m%d%Y')+'_12z.csv has been deleted')
    else:
        pass
        
    if os.path.exists('seaspace_zone1_'+now.strftime('%m%d%Y')+'_00z.csv'):
        os.remove('seaspace_zone1_'+now.strftime('%m%d%Y')+'_00z.csv')
        print('seaspace_zone1_'+now.strftime('%m%d%Y')+'_00z.csv has been deleted')
    else:
        pass

    if os.path.exists('seaspace_zone1_'+yday.strftime('%m%d%Y')+'_12z.csv'):
        os.remove('seaspace_zone1_'+yday.strftime('%m%d%Y')+'_12z.csv')
        print('seaspace_zone1_'+yday.strftime('%m%d%Y')+'_12z.csv has been deleted')
    else:
        pass
        
    if os.path.exists('seaspace_zone1_'+yday.strftime('%m%d%Y')+'_00z.csv'):
        os.remove('seaspace_zone1_'+yday.strftime('%m%d%Y')+'_00z.csv')
        print('seaspace_zone1_'+yday.strftime('%m%d%Y')+'_00z.csv has been deleted')
    else:
        pass   

    
    # Zone 2
    if os.path.exists('seaspace_zone2_'+now.strftime('%m%d%Y')+'_12z.csv'):
        os.remove('seaspace_zone2_'+now.strftime('%m%d%Y')+'_12z.csv')
        print('seaspace_zone2_'+now.strftime('%m%d%Y')+'_12z.csv has been deleted')
    else:
        pass
        
    if os.path.exists('seaspace_zone2_'+now.strftime('%m%d%Y')+'_00z.csv'):
        os.remove('seaspace_zone2_'+now.strftime('%m%d%Y')+'_00z.csv')
        print('seaspace_zone2_'+now.strftime('%m%d%Y')+'_00z.csv has been deleted')
    else:
        pass

    if os.path.exists('seaspace_zone2_'+yday.strftime('%m%d%Y')+'_12z.csv'):
        os.remove('seaspace_zone2_'+yday.strftime('%m%d%Y')+'_12z.csv')
        print('seaspace_zone2_'+yday.strftime('%m%d%Y')+'_12z.csv has been deleted')
    else:
        pass
        
    if os.path.exists('seaspace_zone2_'+yday.strftime('%m%d%Y')+'_00z.csv'):
        os.remove('seaspace_zone2_'+yday.strftime('%m%d%Y')+'_00z.csv')
        print('seaspace_zone2_'+yday.strftime('%m%d%Y')+'_00z.csv has been deleted')
    else:
        pass   
    
    # Zone 3
    if os.path.exists('seaspace_zone3_'+now.strftime('%m%d%Y')+'_12z.csv'):
        os.remove('seaspace_zone3_'+now.strftime('%m%d%Y')+'_12z.csv')
        print('seaspace_zone3_'+now.strftime('%m%d%Y')+'_12z.csv has been deleted')
    else:
        pass
        
    if os.path.exists('seaspace_zone3_'+now.strftime('%m%d%Y')+'_00z.csv'):
        os.remove('seaspace_zone3_'+now.strftime('%m%d%Y')+'_00z.csv')
        print('seaspace_zone3_'+now.strftime('%m%d%Y')+'_00z.csv has been deleted')
    else:
        pass

    if os.path.exists('seaspace_zone3_'+yday.strftime('%m%d%Y')+'_12z.csv'):
        os.remove('seaspace_zone3_'+yday.strftime('%m%d%Y')+'_12z.csv')
        print('seaspace_zone3_'+yday.strftime('%m%d%Y')+'_12z.csv has been deleted')
    else:
        pass
        
    if os.path.exists('seaspace_zone3_'+yday.strftime('%m%d%Y')+'_00z.csv'):
        os.remove('seaspace_zone3_'+yday.strftime('%m%d%Y')+'_00z.csv')
        print('seaspace_zone3_'+yday.strftime('%m%d%Y')+'_00z.csv has been deleted')
    else:
        pass  

    # Zone 4
    
    if os.path.exists('seaspace_zone4_'+now.strftime('%m%d%Y')+'_12z.csv'):
        os.remove('seaspace_zone4_'+now.strftime('%m%d%Y')+'_12z.csv')
        print('seaspace_zone4_'+now.strftime('%m%d%Y')+'_12z.csv has been deleted')
        print('\n')
    else:
        pass
        
    if os.path.exists('seaspace_zone4_'+now.strftime('%m%d%Y')+'_00z.csv'):
        os.remove('seaspace_zone4_'+now.strftime('%m%d%Y')+'_00z.csv')
        print('seaspace_zone4_'+now.strftime('%m%d%Y')+'_00z.csv has been deleted')
        print('\n')
    else:
        pass

    if os.path.exists('seaspace_zone4_'+yday.strftime('%m%d%Y')+'_12z.csv'):
        os.remove('seaspace_zone4_'+yday.strftime('%m%d%Y')+'_12z.csv')
        print('seaspace_zone4_'+yday.strftime('%m%d%Y')+'_12z.csv has been deleted')
        print('\n')
    else:
        pass
        
    if os.path.exists('seaspace_zone4_'+yday.strftime('%m%d%Y')+'_00z.csv'):
        os.remove('seaspace_zone4_'+yday.strftime('%m%d%Y')+'_00z.csv')
        print('seaspace_zone4_'+yday.strftime('%m%d%Y')+'_00z.csv has been deleted')
        print('\n')
    else:
        pass   
        
    
    '''
    In this section we download the new SAWTI CSV files
    '''
    # Zone 1
    try:
        urllib.request.urlretrieve('https://sdge.sdsc.edu/data/sdge/sawti/Zone1-LA-Ventura/seaspace_zone1_'+now.strftime('%m%d%Y')+'_12z.csv', 'seaspace_zone1_'+now.strftime('%m%d%Y')+'_12z.csv')
        print('seaspace_zone1_'+now.strftime('%m%d%Y')+'_12z.csv has been downloaded')
    except Exception as e:
        try:
            urllib.request.urlretrieve('https://sdge.sdsc.edu/data/sdge/sawti/Zone1-LA-Ventura/seaspace_zone1_'+now.strftime('%m%d%Y')+'_00z.csv', 'seaspace_zone1_'+now.strftime('%m%d%Y')+'_00z.csv')
            print('seaspace_zone1_'+now.strftime('%m%d%Y')+'_00z.csv has been downloaded')
        except Exception as e:
            try:
                urllib.request.urlretrieve('https://sdge.sdsc.edu/data/sdge/sawti/Zone1-LA-Ventura/seaspace_zone1_'+yday.strftime('%m%d%Y')+'_12z.csv', 'seaspace_zone1_'+yday.strftime('%m%d%Y')+'_12z.csv')
                print('seaspace_zone1_'+yday.strftime('%m%d%Y')+'_12z.csv has been downloaded')
            except Exception as e:
                pass
    
    # Zone 2
    try:
        urllib.request.urlretrieve('https://sdge.sdsc.edu/data/sdge/sawti/Zone2-Orange-InlandEmpire/seaspace_zone2_'+now.strftime('%m%d%Y')+'_12z.csv', 'seaspace_zone2_'+now.strftime('%m%d%Y')+'_12z.csv')
        print('seaspace_zone2_'+now.strftime('%m%d%Y')+'_12z.csv has been downloaded')
    except Exception as e:
        try:
            urllib.request.urlretrieve('https://sdge.sdsc.edu/data/sdge/sawti/Zone2-Orange-InlandEmpire/seaspace_zone2_'+now.strftime('%m%d%Y')+'_00z.csv', 'seaspace_zone2_'+now.strftime('%m%d%Y')+'_00z.csv')
            print('seaspace_zone2_'+now.strftime('%m%d%Y')+'_00z.csv has been downloaded')
        except Exception as e:
            try:
                urllib.request.urlretrieve('https://sdge.sdsc.edu/data/sdge/sawti/Zone2-Orange-InlandEmpire/seaspace_zone2_'+yday.strftime('%m%d%Y')+'_12z.csv', 'seaspace_zone2_'+yday.strftime('%m%d%Y')+'_12z.csv')
                print('seaspace_zone2_'+yday.strftime('%m%d%Y')+'_12z.csv has been downloaded')
            except Exception as e:
                pass
    
    # Zone 3
    try:
        urllib.request.urlretrieve('https://sdge.sdsc.edu/data/sdge/sawti/Zone3-SanDiego/seaspace_zone3_'+now.strftime('%m%d%Y')+'_12z.csv', 'seaspace_zone3_'+now.strftime('%m%d%Y')+'_12z.csv')
        print('seaspace_zone3_'+now.strftime('%m%d%Y')+'_12z.csv has been downloaded')
    except Exception as e:
        try:
            urllib.request.urlretrieve('https://sdge.sdsc.edu/data/sdge/sawti/Zone3-SanDiego/seaspace_zone3_'+now.strftime('%m%d%Y')+'_00z.csv', 'seaspace_zone3_'+now.strftime('%m%d%Y')+'_00z.csv')
            print('seaspace_zone3_'+now.strftime('%m%d%Y')+'_00z.csv has been downloaded')
        except Exception as e:
            try:
                urllib.request.urlretrieve('https://sdge.sdsc.edu/data/sdge/sawti/Zone3-SanDiego/seaspace_zone3_'+yday.strftime('%m%d%Y')+'_12z.csv', 'seaspace_zone3_'+yday.strftime('%m%d%Y')+'_12z.csv')
                print('seaspace_zone3_'+yday.strftime('%m%d%Y')+'_12z.csv has been downloaded')
            except Exception as e:
                pass
    
    # Zone 4
    try:
        urllib.request.urlretrieve('https://sdge.sdsc.edu/data/sdge/sawti/Zone4-SantaBarbara/seaspace_zone4_'+now.strftime('%m%d%Y')+'_12z.csv', 'seaspace_zone4_'+now.strftime('%m%d%Y')+'_12z.csv')
        print('seaspace_zone4_'+now.strftime('%m%d%Y')+'_12z.csv has been downloaded')
        print("\n")
    except Exception as e:
        try:
            urllib.request.urlretrieve('https://sdge.sdsc.edu/data/sdge/sawti/Zone4-SantaBarbara/seaspace_zone4_'+now.strftime('%m%d%Y')+'_00z.csv', 'seaspace_zone4_'+now.strftime('%m%d%Y')+'_00z.csv')
            print('seaspace_zone4_'+now.strftime('%m%d%Y')+'_00z.csv has been downloaded')
            print("\n")
        except Exception as e:
            try:
                urllib.request.urlretrieve('https://sdge.sdsc.edu/data/sdge/sawti/Zone4-SantaBarbara/seaspace_zone4_'+yday.strftime('%m%d%Y')+'_12z.csv', 'seaspace_zone4_'+yday.strftime('%m%d%Y')+'_12z.csv')
                print('seaspace_zone4_'+yday.strftime('%m%d%Y')+'_12z.csv has been downloaded')
                print("\n")
            except Exception as e:
                pass
    
    try:
        df1 = pd.read_csv('seaspace_zone1_'+now.strftime('%m%d%Y')+'_12z.csv')
        df1 = df1.transpose()
        print('seaspace_zone1_'+now.strftime('%m%d%Y')+'_12z.csv has been converted to a dataframe')
    except Exception as e:
        try:
            df1 = pd.read_csv('seaspace_zone1_'+now.strftime('%m%d%Y')+'_00z.csv')
            df1 = df1.transpose()
            print('seaspace_zone1_'+now.strftime('%m%d%Y')+'_00z.csv has been converted to a dataframe')
        except Exception as e:
            try:
                df1 = pd.read_csv('seaspace_zone1_'+yday.strftime('%m%d%Y')+'_12z.csv')
                df1 = df1.transpose()
                print('seaspace_zone1_'+yday.strftime('%m%d%Y')+'_12z.csv has been converted to a dataframe')
            except Exception as e:
                pass
    
    try:
        df2 = pd.read_csv('seaspace_zone2_'+now.strftime('%m%d%Y')+'_12z.csv')
        df2 = df2.transpose()
        print('seaspace_zone2_'+now.strftime('%m%d%Y')+'_12z.csv has been converted to a dataframe')
    except Exception as e:
        try:
            df2 = pd.read_csv('seaspace_zone2_'+now.strftime('%m%d%Y')+'_00z.csv')
            df2 = df2.transpose()
            print('seaspace_zone2_'+now.strftime('%m%d%Y')+'_00z.csv has been converted to a dataframe')
        except Exception as e:
            try:
                df2 = pd.read_csv('seaspace_zone2_'+yday.strftime('%m%d%Y')+'_12z.csv')
                df2 = df2.transpose()
                print('seaspace_zone2_'+yday.strftime('%m%d%Y')+'_12z.csv has been converted to a dataframe')
            except Exception as e:
                pass
    
    try:
        df3 = pd.read_csv('seaspace_zone3_'+now.strftime('%m%d%Y')+'_12z.csv')
        df3 = df3.transpose()
        print('seaspace_zone3_'+now.strftime('%m%d%Y')+'_12z.csv has been converted to a dataframe')
    except Exception as e:
        try:
            df3 = pd.read_csv('seaspace_zone3_'+now.strftime('%m%d%Y')+'_00z.csv')
            df3 = df3.transpose()
            print('seaspace_zone3_'+now.strftime('%m%d%Y')+'_00z.csv has been converted to a dataframe')
        except Exception as e:
            try:
                df3 = pd.read_csv('seaspace_zone3_'+yday.strftime('%m%d%Y')+'_12z.csv')
                df3 = df3.transpose()
                print('seaspace_zone3_'+yday.strftime('%m%d%Y')+'_12z.csv has been converted to a dataframe')
            except Exception as e:
                pass
    
    try:
        df4 = pd.read_csv('seaspace_zone4_'+now.strftime('%m%d%Y')+'_12z.csv')
        df4 = df4.transpose()
        print('seaspace_zone4_'+now.strftime('%m%d%Y')+'_12z.csv has been converted to a dataframe')
        print("\n")
    except Exception as e:
        try:
            df4 = pd.read_csv('seaspace_zone4_'+now.strftime('%m%d%Y')+'_00z.csv')
            df4 = df4.transpose()
            print('seaspace_zone1_'+now.strftime('%m%d%Y')+'_00z.csv has been converted to a dataframe')
            print("\n")
        except Exception as e:
            try:
                df4 = pd.read_csv('seaspace_zone4_'+yday.strftime('%m%d%Y')+'_12z.csv')
                df4 = df4.transpose()
                print('seaspace_zone4_'+yday.strftime('%m%d%Y')+'_12z.csv has been converted to a dataframe')
                print("\n")
            except Exception as e:
                pass

    dates = []
    dates.append(now)
    dates.append(day2)
    dates.append(day3)
    dates.append(day4)
    dates.append(day5)
    dates.append(day6)
    dates.append(day7)
        
    try:

        z1_FMC_1 = zone_1_FMC_weight * df1['FMC'].iloc[0]
        if z1_FMC_1 > 1:
            z1_FMC_1 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z1_FMC_1 = z1_FMC_1

        z1_FMC_2 = zone_1_FMC_weight * df1['FMC'].iloc[1]
        if z1_FMC_2 > 1:
            z1_FMC_2 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z1_FMC_2 = z1_FMC_2

        z1_FMC_3 = zone_1_FMC_weight * df1['FMC'].iloc[2]
        if z1_FMC_3 > 1:
            z1_FMC_3 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z1_FMC_3 = z1_FMC_3

        z1_FMC_4 = zone_1_FMC_weight * df1['FMC'].iloc[3]
        if z1_FMC_4 > 1:
            z1_FMC_4 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z1_FMC_4 = z1_FMC_4

        z1_FMC_5 = zone_1_FMC_weight * df1['FMC'].iloc[4]
        if z1_FMC_5 > 1:
            z1_FMC_5 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z1_FMC_5 = z1_FMC_5

        z1_FMC_6 = zone_1_FMC_weight * df1['FMC'].iloc[5]
        if z1_FMC_6 > 1:
            z1_FMC_6 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z1_FMC_6 = z1_FMC_6

        z1_FMC_7 = zone_1_FMC_weight * df1['FMC'].iloc[6]
        if z1_FMC_7 > 1:
            z1_FMC_7 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
            print("\n")
        else:
            z1_FMC_7 = z1_FMC_7
        
        LFP1_Day1 = round((0.001) * (zone_1_W_weight * df1['W^2'].iloc[0]) * (zone_1_DD_weight * df1['DD'].iloc[0]) * (z1_FMC_1), 0)
        LFP1_Day2 = round((0.001) * (zone_1_W_weight * df1['W^2'].iloc[1]) * (zone_1_DD_weight * df1['DD'].iloc[1]) * (z1_FMC_2), 0)
        LFP1_Day3 = round((0.001) * (zone_1_W_weight * df1['W^2'].iloc[2]) * (zone_1_DD_weight * df1['DD'].iloc[2]) * (z1_FMC_3), 0)
        LFP1_Day4 = round((0.001) * (zone_1_W_weight * df1['W^2'].iloc[3]) * (zone_1_DD_weight * df1['DD'].iloc[3]) * (z1_FMC_4), 0)
        LFP1_Day5 = round((0.001) * (zone_1_W_weight * df1['W^2'].iloc[4]) * (zone_1_DD_weight * df1['DD'].iloc[4]) * (z1_FMC_5), 0)
        LFP1_Day6 = round((0.001) * (zone_1_W_weight * df1['W^2'].iloc[5]) * (zone_1_DD_weight * df1['DD'].iloc[5]) * (z1_FMC_6), 0)
        LFP1_Day7 = round((0.001) * (zone_1_W_weight * df1['W^2'].iloc[6]) * (zone_1_DD_weight * df1['DD'].iloc[6]) * (z1_FMC_7), 0)
        print("LFP Zone 1 (Day 1 - Date: "+dates[0].strftime('%m/%d/%Y)')+": "+str(LFP1_Day1))
        print("LFP Zone 1 (Day 2 - Date: "+dates[1].strftime('%m/%d/%Y)')+": "+str(LFP1_Day2))
        print("LFP Zone 1 (Day 3 - Date: "+dates[2].strftime('%m/%d/%Y)')+": "+str(LFP1_Day3))
        print("LFP Zone 1 (Day 4 - Date: "+dates[3].strftime('%m/%d/%Y)')+": "+str(LFP1_Day4))
        print("LFP Zone 1 (Day 5 - Date: "+dates[4].strftime('%m/%d/%Y)')+": "+str(LFP1_Day5))
        print("LFP Zone 1 (Day 6 - Date: "+dates[5].strftime('%m/%d/%Y)')+": "+str(LFP1_Day6))
        print("LFP Zone 1 (Day 7 - Date: "+dates[6].strftime('%m/%d/%Y)')+": "+str(LFP1_Day7))
        print('\n')
        zone_1_LFP_values = []
        zone_1_LFP_values.append(LFP1_Day1)
        zone_1_LFP_values.append(LFP1_Day2)
        zone_1_LFP_values.append(LFP1_Day3)
        zone_1_LFP_values.append(LFP1_Day4)
        zone_1_LFP_values.append(LFP1_Day5)
        zone_1_LFP_values.append(LFP1_Day6)
        zone_1_LFP_values.append(LFP1_Day7)
    except Exception as e:
        pass
    
    try:

        z2_FMC_1 = zone_2_FMC_weight * df2['FMC'].iloc[0]
        if z2_FMC_1 > 1:
            z2_FMC_1 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z2_FMC_1 = z2_FMC_1

        z2_FMC_2 = zone_2_FMC_weight * df2['FMC'].iloc[1]
        if z2_FMC_2 > 1:
            z2_FMC_2 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z2_FMC_2 = z2_FMC_2

        z2_FMC_3 = zone_2_FMC_weight * df2['FMC'].iloc[2]
        if z2_FMC_3 > 1:
            z2_FMC_3 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z2_FMC_3 = z2_FMC_3

        z2_FMC_4 = zone_2_FMC_weight * df2['FMC'].iloc[3]
        if z2_FMC_4 > 1:
            z2_FMC_4 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z2_FMC_4 = z2_FMC_4

        z2_FMC_5 = zone_2_FMC_weight * df2['FMC'].iloc[4]
        if z2_FMC_5 > 1:
            z2_FMC_5 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z2_FMC_5 = z2_FMC_5

        z2_FMC_6 = zone_2_FMC_weight * df2['FMC'].iloc[5]
        if z2_FMC_6 > 1:
            z2_FMC_6 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z2_FMC_6 = z2_FMC_6

        z2_FMC_7 = zone_2_FMC_weight * df2['FMC'].iloc[6]
        if z2_FMC_7 > 1:
            z2_FMC_7 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
            print("\n")
        else:
            z2_FMC_7 = z2_FMC_7

        LFP2_Day1 = round((0.001) * (zone_2_W_weight * df2['W^2'].iloc[0]) * (zone_2_DD_weight * df2['DD'].iloc[0]) * (z2_FMC_1), 0)
        LFP2_Day2 = round((0.001) * (zone_2_W_weight * df2['W^2'].iloc[1]) * (zone_2_DD_weight * df2['DD'].iloc[1]) * (z2_FMC_2), 0)
        LFP2_Day3 = round((0.001) * (zone_2_W_weight * df2['W^2'].iloc[2]) * (zone_2_DD_weight * df2['DD'].iloc[2]) * (z2_FMC_3), 0)
        LFP2_Day4 = round((0.001) * (zone_2_W_weight * df2['W^2'].iloc[3]) * (zone_2_DD_weight * df2['DD'].iloc[3]) * (z2_FMC_4), 0)
        LFP2_Day5 = round((0.001) * (zone_2_W_weight * df2['W^2'].iloc[4]) * (zone_2_DD_weight * df2['DD'].iloc[4]) * (z2_FMC_5), 0)
        LFP2_Day6 = round((0.001) * (zone_2_W_weight * df2['W^2'].iloc[5]) * (zone_2_DD_weight * df2['DD'].iloc[5]) * (z2_FMC_6), 0)
        LFP2_Day7 = round((0.001) * (zone_2_W_weight * df2['W^2'].iloc[6]) * (zone_2_DD_weight * df2['DD'].iloc[6]) * (z2_FMC_7), 0)
        print("LFP Zone 2 (Day 1 - Date: "+dates[0].strftime('%m/%d/%Y)')+": "+str(LFP2_Day1))
        print("LFP Zone 2 (Day 2 - Date: "+dates[1].strftime('%m/%d/%Y)')+": "+str(LFP2_Day2))
        print("LFP Zone 2 (Day 3 - Date: "+dates[2].strftime('%m/%d/%Y)')+": "+str(LFP2_Day3))
        print("LFP Zone 2 (Day 4 - Date: "+dates[3].strftime('%m/%d/%Y)')+": "+str(LFP2_Day4))
        print("LFP Zone 2 (Day 5 - Date: "+dates[4].strftime('%m/%d/%Y)')+": "+str(LFP2_Day5))
        print("LFP Zone 2 (Day 6 - Date: "+dates[5].strftime('%m/%d/%Y)')+": "+str(LFP2_Day6))
        print("LFP Zone 2 (Day 7 - Date: "+dates[6].strftime('%m/%d/%Y)')+": "+str(LFP2_Day7))
        print('\n')
        zone_2_LFP_values = []
        zone_2_LFP_values.append(LFP2_Day1)
        zone_2_LFP_values.append(LFP2_Day2)
        zone_2_LFP_values.append(LFP2_Day3)
        zone_2_LFP_values.append(LFP2_Day4)
        zone_2_LFP_values.append(LFP2_Day5)
        zone_2_LFP_values.append(LFP2_Day6)
        zone_2_LFP_values.append(LFP2_Day7)
    except Exception as e:
        pass
    
    try:

        z3_FMC_1 = zone_3_FMC_weight * df3['FMC'].iloc[0]
        if z3_FMC_1 > 1:
            z3_FMC_1 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z3_FMC_1 = z3_FMC_1

        z3_FMC_2 = zone_3_FMC_weight * df3['FMC'].iloc[1]
        if z3_FMC_2 > 1:
            z3_FMC_2 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z3_FMC_2 = z3_FMC_2

        z3_FMC_3 = zone_3_FMC_weight * df3['FMC'].iloc[2]
        if z3_FMC_3 > 1:
            z3_FMC_3 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z3_FMC_3 = z3_FMC_3

        z3_FMC_4 = zone_3_FMC_weight * df3['FMC'].iloc[3]
        if z3_FMC_4 > 1:
            z3_FMC_4 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z3_FMC_4 = z3_FMC_4

        z3_FMC_5 = zone_3_FMC_weight * df3['FMC'].iloc[4]
        if z3_FMC_5 > 1:
            z3_FMC_5 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z3_FMC_5 = z3_FMC_5

        z3_FMC_6 = zone_3_FMC_weight * df3['FMC'].iloc[5]
        if z3_FMC_6 > 1:
            z3_FMC_6 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z3_FMC_6 = z3_FMC_6

        z3_FMC_7 = zone_3_FMC_weight * df3['FMC'].iloc[6]
        if z3_FMC_7 > 1:
            z3_FMC_7 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
            print("\n")
        else:
            z3_FMC_7 = z3_FMC_7
        
        LFP3_Day1 = round((0.001) * (zone_3_W_weight * df3['W^2'].iloc[0]) * (zone_3_DD_weight * df3['DD'].iloc[0]) * (z3_FMC_1), 0)
        LFP3_Day2 = round((0.001) * (zone_3_W_weight * df3['W^2'].iloc[1]) * (zone_3_DD_weight * df3['DD'].iloc[1]) * (z3_FMC_2), 0)
        LFP3_Day3 = round((0.001) * (zone_3_W_weight * df3['W^2'].iloc[2]) * (zone_3_DD_weight * df3['DD'].iloc[2]) * (z3_FMC_3), 0)
        LFP3_Day4 = round((0.001) * (zone_3_W_weight * df3['W^2'].iloc[3]) * (zone_3_DD_weight * df3['DD'].iloc[3]) * (z3_FMC_4), 0)
        LFP3_Day5 = round((0.001) * (zone_3_W_weight * df3['W^2'].iloc[4]) * (zone_3_DD_weight * df3['DD'].iloc[4]) * (z3_FMC_5), 0)
        LFP3_Day6 = round((0.001) * (zone_3_W_weight * df3['W^2'].iloc[5]) * (zone_3_DD_weight * df3['DD'].iloc[5]) * (z3_FMC_6), 0)
        LFP3_Day7 = round((0.001) * (zone_3_W_weight * df3['W^2'].iloc[6]) * (zone_3_DD_weight * df3['DD'].iloc[6]) * (z3_FMC_7), 0)
        print("LFP Zone 3 (Day 1 - Date: "+dates[0].strftime('%m/%d/%Y)')+": "+str(LFP3_Day1))
        print("LFP Zone 3 (Day 2 - Date: "+dates[1].strftime('%m/%d/%Y)')+": "+str(LFP3_Day2))
        print("LFP Zone 3 (Day 3 - Date: "+dates[2].strftime('%m/%d/%Y)')+": "+str(LFP3_Day3))
        print("LFP Zone 3 (Day 4 - Date: "+dates[3].strftime('%m/%d/%Y)')+": "+str(LFP3_Day4))
        print("LFP Zone 3 (Day 5 - Date: "+dates[4].strftime('%m/%d/%Y)')+": "+str(LFP3_Day5))
        print("LFP Zone 3 (Day 6 - Date: "+dates[5].strftime('%m/%d/%Y)')+": "+str(LFP3_Day6))
        print("LFP Zone 3 (Day 7 - Date: "+dates[6].strftime('%m/%d/%Y)')+": "+str(LFP3_Day7))
        print('\n')
        zone_3_LFP_values = []
        zone_3_LFP_values.append(LFP3_Day1)
        zone_3_LFP_values.append(LFP3_Day2)
        zone_3_LFP_values.append(LFP3_Day3)
        zone_3_LFP_values.append(LFP3_Day4)
        zone_3_LFP_values.append(LFP3_Day5)
        zone_3_LFP_values.append(LFP3_Day6)
        zone_3_LFP_values.append(LFP3_Day7)
    except Exception as e:
        pass
    
    try:

        z4_FMC_1 = zone_4_FMC_weight * df4['FMC'].iloc[0]
        if z4_FMC_1 > 1:
            z4_FMC_1 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z4_FMC_1 = z4_FMC_1

        z4_FMC_2 = zone_4_FMC_weight * df4['FMC'].iloc[1]
        if z4_FMC_2 > 1:
            z4_FMC_2 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z4_FMC_2 = z4_FMC_2

        z4_FMC_3 = zone_4_FMC_weight * df4['FMC'].iloc[2]
        if z4_FMC_3 > 1:
            z4_FMC_3 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z4_FMC_3 = z4_FMC_3

        z4_FMC_4 = zone_4_FMC_weight * df4['FMC'].iloc[3]
        if z4_FMC_4 > 1:
            z4_FMC_4 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z4_FMC_4 = z4_FMC_4

        z4_FMC_5 = zone_4_FMC_weight * df4['FMC'].iloc[4]
        if z4_FMC_5 > 1:
            z4_FMC_5 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z4_FMC_5 = z4_FMC_5

        z4_FMC_6 = zone_3_FMC_weight * df3['FMC'].iloc[5]
        if z4_FMC_6 > 1:
            z4_FMC_6 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
        else:
            z4_FMC_6 = z4_FMC_6

        z4_FMC_7 = zone_4_FMC_weight * df4['FMC'].iloc[6]
        if z4_FMC_7 > 1:
            z4_FMC_7 = 1
            print("FMC ranges between 0 and 1. The weight applied puts this value over 1. Setting the FMC value to 1.")
            print("\n")
        else:
            z4_FMC_7 = z4_FMC_7
        
        LFP4_Day1 = round((0.001) * (zone_4_W_weight * df4['W^2'].iloc[0]) * (zone_4_DD_weight * df4['DD'].iloc[0]) * (z4_FMC_1), 0)
        LFP4_Day2 = round((0.001) * (zone_4_W_weight * df4['W^2'].iloc[1]) * (zone_4_DD_weight * df4['DD'].iloc[1]) * (z4_FMC_2), 0)
        LFP4_Day3 = round((0.001) * (zone_4_W_weight * df4['W^2'].iloc[2]) * (zone_4_DD_weight * df4['DD'].iloc[2]) * (z4_FMC_3), 0)
        LFP4_Day4 = round((0.001) * (zone_4_W_weight * df4['W^2'].iloc[3]) * (zone_4_DD_weight * df4['DD'].iloc[3]) * (z4_FMC_4), 0)
        LFP4_Day5 = round((0.001) * (zone_4_W_weight * df4['W^2'].iloc[4]) * (zone_4_DD_weight * df4['DD'].iloc[4]) * (z4_FMC_5), 0)
        LFP4_Day6 = round((0.001) * (zone_4_W_weight * df4['W^2'].iloc[5]) * (zone_4_DD_weight * df4['DD'].iloc[5]) * (z4_FMC_6), 0)
        LFP4_Day7 = round((0.001) * (zone_4_W_weight * df4['W^2'].iloc[6]) * (zone_4_DD_weight * df4['DD'].iloc[6]) * (z4_FMC_7), 0)
        print("LFP Zone 4 (Day 1 - Date: "+dates[0].strftime('%m/%d/%Y)')+": "+str(LFP4_Day1))
        print("LFP Zone 4 (Day 2 - Date: "+dates[1].strftime('%m/%d/%Y)')+": "+str(LFP4_Day2))
        print("LFP Zone 4 (Day 3 - Date: "+dates[2].strftime('%m/%d/%Y)')+": "+str(LFP4_Day3))
        print("LFP Zone 4 (Day 4 - Date: "+dates[3].strftime('%m/%d/%Y)')+": "+str(LFP4_Day4))
        print("LFP Zone 4 (Day 5 - Date: "+dates[4].strftime('%m/%d/%Y)')+": "+str(LFP4_Day5))
        print("LFP Zone 4 (Day 6 - Date: "+dates[5].strftime('%m/%d/%Y)')+": "+str(LFP4_Day6))
        print("LFP Zone 4 (Day 7 - Date: "+dates[6].strftime('%m/%d/%Y)')+": "+str(LFP4_Day7))
        zone_4_LFP_values = []
        zone_4_LFP_values.append(LFP4_Day1)
        zone_4_LFP_values.append(LFP4_Day2)
        zone_4_LFP_values.append(LFP4_Day3)
        zone_4_LFP_values.append(LFP4_Day4)
        zone_4_LFP_values.append(LFP4_Day5)
        zone_4_LFP_values.append(LFP4_Day6)
        zone_4_LFP_values.append(LFP4_Day7)
    except Exception as e:
        pass

    local = datetime.now()
    timezone = pytz.timezone('America/Los_Angeles')
    now_la = local.astimezone(timezone)
    hour = now_la.hour

    plt.style.use('seaborn-v0_8-darkgrid')
    
    fig = plt.figure(figsize=(12,10))
    fig.set_facecolor('aliceblue')
    fig.suptitle("Santa Ana Wildfire Threat Index (SAWTI)", fontsize=16, fontweight='bold')
    
    ax1 = fig.add_subplot(2, 2, 1)
    if hour > 10 and hour < 22:
        ax1.bar(dates, zone_1_LFP_values, color='red', align='center', zorder=2, width=0.4)
    if hour >= 22 or hour <= 10:
        ax1.bar(dates, zone_1_LFP_values, color='red', align='edge', zorder=2, width=0.4)
    ax1.set_title("Zone 1: Los Angeles & Ventura", fontweight='bold')
    ax1.set_xlabel("Date", fontweight='bold')
    ax1.xaxis.set_major_formatter(md.DateFormatter('%a %m/%d'))
    ax1.set_ylabel("Large Fire Potential", fontweight='bold')
    ax1.set_ylim(0, 60)
    ax1.axhspan(0, zone_1_threshold_1, color='green', alpha=0.3, zorder=1)
    ax1.axhspan(zone_1_threshold_1, zone_1_threshold_2, color='yellow', alpha=0.3, zorder=1)
    ax1.axhspan(zone_1_threshold_2, zone_1_threshold_3, color='orange', alpha=0.3, zorder=1)
    ax1.axhspan(zone_1_threshold_3, zone_1_threshold_4, color='red', alpha=0.3, zorder=1)
    ax1.axhspan(zone_1_threshold_4, 60, color='purple', alpha=0.3, zorder=1)

    ax2 = fig.add_subplot(2, 2, 2)
    if hour > 10 and hour < 22:
        ax2.bar(dates, zone_2_LFP_values, color='red', align='center', zorder=2, width=0.4)
    if hour >= 22 or hour <= 10:
        ax2.bar(dates, zone_2_LFP_values, color='red', align='edge', zorder=2, width=0.4)
    ax2.set_title("Zone 2: Orange County & Inland Empire", fontweight='bold')
    ax2.set_xlabel("Date", fontweight='bold')
    ax2.xaxis.set_major_formatter(md.DateFormatter('%a %m/%d'))
    ax2.set_ylabel("Large Fire Potential", fontweight='bold')
    ax2.set_ylim(0, 60)
    ax2.axhspan(0, zone_2_threshold_1, color='green', alpha=0.3, zorder=1)
    ax2.axhspan(zone_2_threshold_1, zone_2_threshold_2, color='yellow', alpha=0.3, zorder=1)
    ax2.axhspan(zone_2_threshold_2, zone_2_threshold_3, color='orange', alpha=0.3, zorder=1)
    ax2.axhspan(zone_2_threshold_3, zone_2_threshold_4, color='red', alpha=0.3, zorder=1)
    ax2.axhspan(zone_2_threshold_4, 60, color='purple', alpha=0.3, zorder=1)

    ax3 = fig.add_subplot(2, 2, 3)
    if hour > 10 and hour < 22:
        ax3.bar(dates, zone_3_LFP_values, color='red', align='center', zorder=2, width=0.4)
    if hour >= 22 or hour <= 10:
        ax3.bar(dates, zone_3_LFP_values, color='red', align='edge', zorder=2, width=0.4)
    ax3.set_title("Zone 3: San Diego", fontweight='bold')
    ax3.set_xlabel("Date", fontweight='bold')
    ax3.xaxis.set_major_formatter(md.DateFormatter('%a %m/%d'))
    ax3.set_ylabel("Large Fire Potential", fontweight='bold')
    ax3.set_ylim(0, 60)
    ax3.axhspan(0, zone_3_threshold_1, color='green', alpha=0.3, zorder=1)
    ax3.axhspan(zone_3_threshold_1, zone_3_threshold_2, color='yellow', alpha=0.3, zorder=1)
    ax3.axhspan(zone_3_threshold_2, zone_3_threshold_3, color='orange', alpha=0.3, zorder=1)
    ax3.axhspan(zone_3_threshold_3, zone_3_threshold_4, color='red', alpha=0.3, zorder=1)
    ax3.axhspan(zone_3_threshold_4, 60, color='purple', alpha=0.3, zorder=1)

    ax4 = fig.add_subplot(2, 2, 4)
    if hour > 10 and hour < 22:
        ax4.bar(dates, zone_4_LFP_values, color='red', align='center', zorder=2, width=0.4)
    if hour >= 22 or hour <= 10:
        ax4.bar(dates, zone_4_LFP_values, color='red', align='edge', zorder=2, width=0.4)
    ax4.set_title("Zone 4: Santa Barbara", fontweight='bold')
    ax4.set_xlabel("Date", fontweight='bold')
    ax4.xaxis.set_major_formatter(md.DateFormatter('%a %m/%d'))
    ax4.set_ylabel("Large Fire Potential", fontweight='bold')
    ax4.set_ylim(0, 60)
    ax4.axhspan(0, zone_4_threshold_1, color='green', alpha=0.3, zorder=1)
    ax4.axhspan(zone_4_threshold_1, zone_4_threshold_2, color='yellow', alpha=0.3, zorder=1)
    ax4.axhspan(zone_4_threshold_2, zone_4_threshold_3, color='orange', alpha=0.3, zorder=1)
    ax4.axhspan(zone_4_threshold_3, zone_4_threshold_4, color='red', alpha=0.3, zorder=1)
    ax4.axhspan(zone_4_threshold_4, 60, color='purple', alpha=0.3, zorder=1)

    props = dict(boxstyle='round', facecolor='wheat', alpha=1)
    box = dict(boxstyle='round', facecolor='lavender', alpha=1)

    fig.text(0.1, 0.05, "Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nData Source: sdge.sdsc.edu\nImage Created: " + local_time.strftime('%m/%d/%Y %H:%M Local') + " (" + utc_time.strftime('%H:%M UTC') + ")", fontsize=12, fontweight='bold', verticalalignment='top', bbox=props, zorder=10)    

    fig.text(0.42, 0.94, "(Rolinski et al. 2016)", fontsize=14, fontweight='roman', verticalalignment='top', zorder=10) 

    fig.text(0.55, 0, f"                                 Weighting of LFP Components By Zone\nZone 1: Wind: {zone_1_W_weight} | Dew Point Depression: {zone_1_DD_weight} | Fuel Moisture Component: {zone_1_FMC_weight}\nZone 2: Wind: {zone_2_W_weight} | Dew Point Depression: {zone_2_DD_weight} | Fuel Moisture Component: {zone_2_FMC_weight}\nZone 3: Wind: {zone_3_W_weight} | Dew Point Depression: {zone_3_DD_weight} | Fuel Moisture Component: {zone_3_FMC_weight}\nZone 4: Wind: {zone_4_W_weight} | Dew Point Depression: {zone_4_DD_weight} | Fuel Moisture Component: {zone_4_FMC_weight}", fontsize=9, fontweight='bold', bbox=box)

    if zone_1_W_weight == 1 and zone_1_DD_weight == 1 and zone_1_FMC_weight == 1 and zone_2_W_weight ==1 and zone_2_DD_weight == 1 and zone_2_FMC_weight == 1 and zone_3_W_weight == 1 and zone_3_DD_weight == 1 and zone_3_FMC_weight == 1 and zone_4_W_weight == 1 and zone_4_DD_weight == 1 and zone_4_FMC_weight == 1:

        fname = 'SAWTI With Normal Weighting.jpg'

    else:

        fname = f"SAWTI With Weights Of {zone_1_W_weight} Zone 1 Wind {zone_1_DD_weight} Zone 1 DD {zone_1_FMC_weight} Zone 1 FMC {zone_2_W_weight} Zone 2 Wind {zone_2_DD_weight} Zone 2 DD {zone_2_FMC_weight} Zone 2 FMC {zone_3_W_weight} Zone 3 Wind {zone_3_DD_weight} Zone 3 DD {zone_3_FMC_weight} Zone 3 FMC {zone_4_W_weight} Zone 4 Wind {zone_4_DD_weight} Zone 4 DD {zone_4_FMC_weight} Zone 4 FMC.jpg"

    if os.path.exists(f"Weather Data"):
        print("Already Satisfied: f:Weather Data Exists.")
        if os.path.exists(f"Weather Data/SAWTI"):
            print("Already Satisfied: f:Weather Data/SAWTI Exists.")
            plt.savefig(f"Weather Data/SAWTI/{fname}", bbox_inches='tight')
            print(f"Image Saved to f:Weather Data/SAWTI/{fname}")
        else:
            print("f:Weather Data/SAWTI does not exist. Building new branch to the existing directory...")
            os.mkdir(f"Weather Data/SAWTI")
            print("Successfully built new branch.")
            plt.savefig(f"Weather Data/SAWTI/{fname}", bbox_inches='tight')
            print(f"Image Saved to f:Weather Data/SAWTI/{fname}")
    else:
        print("f:Weather Data does not exist. Building the directory automatically...")
        os.mkdir(f"Weather Data")
        os.mkdir(f"Weather Data/SAWTI")
        print("Successfully built directory and current branch.")
        plt.savefig(f"Weather Data/SAWTI/{fname}", bbox_inches='tight')
        print(f"Image Saved to f:Weather Data/SAWTI/{fname}")        
