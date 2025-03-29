'''
This file hosts the functions to check for the existence of the CSV files that have the SIGs of the various RAWS stations and data associated with those SIGs.
If the CSV files exist, nothing additional is necessary.

If not, the function in this file will build the directory to host the CSVs and download and save the CSVs to that folder.

This file is written by (C) Meteorologist Eric J. Drewitz (USDA/USFS)

'''
# Imports
import urllib.request
import os
import pandas as pd
import numpy as np

from datetime import datetime, timedelta

def check_folders():
    
    r'''
    This function checks if the folder that will house the CSV files exists.
    If not the folder will be created.

    Required Arguments: None

    Optional Arguments: None

    Returns: A folder that will house the RAWS SIGs CSV files
    '''

    gacc_id = ['OSCC', 'ONCC', 'SWCC', 'AICC', 'NWCC', 'GBCC', 'NRCC', 'RMCC', 'EACC', 'SACC']

    if os.path.exists(f"RAWS SIGs"):
        pass
    else:
        os.mkdir(f"RAWS SIGs")

    for gacc in gacc_id:
        if os.path.exists(f"RAWS SIGs/{gacc}"):
            pass
        else:
            os.mkdir(f"RAWS SIGs/{gacc}")

def get_raws_sig_info():

    r'''
    This function will download the CSV files that have the RAWS SIG Information from my github page if they are not detected
    on the user's computer. 

    Required Arguments: None

    Optional Arguments: None

    Returns: Downloading the RAWS SIG Information CSV files and placing them in the f:RAWS SIGs folder if they aren't there already
    '''

    if os.path.exists(f"RAWS SIGs/OSCC/OSCC_StationList.csv"):
        pass
    else:
        urllib.request.urlretrieve(f"https://raw.githubusercontent.com/edrewitz/firewxpy/refs/heads/main/RAWS%20SIGs/OSCC_StationList.csv", f"OSCC_StationList.csv")
        os.replace(f"OSCC_StationList.csv", f"RAWS SIGs/OSCC/OSCC_StationList.csv")

    if os.path.exists(f"RAWS SIGs/OSCC/OSCC_PSA_Percentiles.csv"):
        pass
    else:
        urllib.request.urlretrieve(f"https://raw.githubusercontent.com/edrewitz/firewxpy/refs/heads/main/RAWS%20SIGs/OSCC_PSA_Percentiles.csv", f"OSCC_PSA_Percentiles.csv")
        os.replace(f"OSCC_PSA_Percentiles.csv", f"RAWS SIGs/OSCC/OSCC_PSA_Percentiles.csv")

check_folders()
get_raws_sig_info()

def get_sigs(gacc_region):

    r'''
    This function returns the information of the SIGs in each GACC Region. 

    Required Arguments: 

    1) gacc_region (String) - The 4-letter GACC Region abbreviation

    Optional Arguments: None

    Returns: Returns the station list for each SIG. 

    '''

    df = pd.read_csv(f"RAWS SIGs/{gacc_region.upper()}/{gacc_region.upper()}_StationList.csv")

    return df


def get_psa_percentiles(gacc_region):

    r'''
    This function will parse through the various RAWS CSV files and calculate the 100-hr DFM, 1000-hr DFM and ERC percentiles by SIG. 

    Required Arguments:

    1) gacc_region (String) - The 4-letter abbreviation of the GACC

    Optional Arguments: None

    Returns: A CSV file hosting all the PSA percentiles saved to f:FEMS Data/{gacc_region}/PSA Percentiles

    '''

    gacc_region = gacc_region.upper()
    
    paths = []
    for folder in os.listdir(f"FEMS Data/Stations/{gacc_region}"):
        path = f"FEMS Data/Stations/{gacc_region}/{folder}"
        paths.append(path)
    
    dfm_100_p_3 = []
    dfm_100_p_10 = []
    dfm_100_p_20 = []
    dfm_100_p_40 = []
    
    dfm_1000_p_3 = []
    dfm_1000_p_10 = []
    dfm_1000_p_20 = []
    dfm_1000_p_40 = []
    
    erc_p_60 = []
    erc_p_80 = []
    erc_p_90 = []
    erc_p_97 = []
    erc_p_99 = []
    
    psas = []
    psa = 0
    for p in range(0, len(paths)):
        files = []
        for file in os.listdir(paths[p]):
            files.append(file)
            
        percent_3_100hr = []
        percent_10_100hr = []
        percent_20_100hr = []
        percent_40_100hr = []
    
        percent_3_1000hr = []
        percent_10_1000hr = []
        percent_20_1000hr = []
        percent_40_1000hr = []
    
        percent_60_erc = []
        percent_80_erc = []
        percent_90_erc = []
        percent_97_erc = []
        percent_99_erc = []
    
        for i in range(0, len(files)):
            try:
                df = pd.read_csv(f"{paths[p]}/{files[i]}")
                
                p3_100 = np.percentile(df['hundredHR_TL_FuelMoisture'], 3)
                percent_3_100hr.append(p3_100)
                p10_100 = np.percentile(df['hundredHR_TL_FuelMoisture'], 10)
                percent_10_100hr.append(p10_100)
                p20_100 = np.percentile(df['hundredHR_TL_FuelMoisture'], 20)
                percent_20_100hr.append(p20_100)
                p40_100 = np.percentile(df['hundredHR_TL_FuelMoisture'], 40)
                percent_40_100hr.append(p40_100)
        
                p3_1000 = np.percentile(df['thousandHR_TL_FuelMoisture'], 3)
                percent_3_1000hr.append(p3_1000)
                p10_1000 = np.percentile(df['thousandHR_TL_FuelMoisture'], 10)
                percent_10_1000hr.append(p10_1000)
                p20_1000 = np.percentile(df['thousandHR_TL_FuelMoisture'], 20)
                percent_20_1000hr.append(p20_1000)
                p40_1000 = np.percentile(df['thousandHR_TL_FuelMoisture'], 40)
                percent_40_1000hr.append(p40_1000)
    
                p60_erc = np.percentile(df['energyReleaseComponent'], 60)
                percent_60_erc.append(p60_erc)
                p80_erc = np.percentile(df['energyReleaseComponent'], 80)
                percent_80_erc.append(p80_erc)
                p90_erc = np.percentile(df['energyReleaseComponent'], 90)
                percent_90_erc.append(p90_erc)
                p97_erc = np.percentile(df['energyReleaseComponent'], 97)
                percent_97_erc.append(p97_erc)
                p99_erc = np.percentile(df['energyReleaseComponent'], 99)
                percent_99_erc.append(p99_erc)
                
            except Exception as e:
                pass
    
    
            
        try:
            mean_3_100 = np.nanmean(percent_3_100hr)
            dfm_100_p_3.append(mean_3_100)
        
            mean_10_100 = np.nanmean(percent_10_100hr)
            dfm_100_p_10.append(mean_10_100)
    
            mean_20_100 = np.nanmean(percent_20_100hr)
            dfm_100_p_20.append(mean_20_100)
    
            mean_40_100 = np.nanmean(percent_40_100hr)
            dfm_100_p_40.append(mean_40_100)
    
            mean_3_1000 = np.nanmean(percent_3_1000hr)
            dfm_1000_p_3.append(mean_3_1000)
        
            mean_10_1000 = np.nanmean(percent_10_1000hr)
            dfm_1000_p_10.append(mean_10_1000)
    
            mean_20_1000 = np.nanmean(percent_20_1000hr)
            dfm_1000_p_20.append(mean_20_1000)
    
            mean_40_1000 = np.nanmean(percent_40_1000hr)
            dfm_1000_p_40.append(mean_40_1000)
    
            mean_60_erc = np.nanmean(percent_60_erc)
            erc_p_60.append(mean_60_erc)
    
            mean_80_erc = np.nanmean(percent_80_erc)
            erc_p_80.append(mean_80_erc)
    
            mean_90_erc = np.nanmean(percent_90_erc)
            erc_p_90.append(mean_90_erc)
    
            mean_97_erc = np.nanmean(percent_97_erc)
            erc_p_97.append(mean_97_erc)
    
            mean_99_erc = np.nanmean(percent_99_erc)
            erc_p_99.append(mean_99_erc)
        
            psa = psa + 1
            psas.append(psa)
        except Exception as e:
            pass

    main = pd.DataFrame()
    
    main['psa'] = psas
    
    main['100hr_DFM_3_percentile'] = dfm_100_p_3
    main['100hr_DFM_10_percentile'] = dfm_100_p_10
    main['100hr_DFM_20_percentile'] = dfm_100_p_20
    main['100hr_DFM_40_percentile'] = dfm_100_p_40
    
    main['1000hr_DFM_3_percentile'] = dfm_1000_p_3
    main['1000hr_DFM_10_percentile'] = dfm_1000_p_10
    main['1000hr_DFM_20_percentile'] = dfm_1000_p_20
    main['1000hr_DFM_40_percentile'] = dfm_1000_p_40
    
    main['ERC_60th_percentile'] = erc_p_60
    main['ERC_80th_percentile'] = erc_p_80
    main['ERC_90th_percentile'] = erc_p_90
    main['ERC_97th_percentile'] = erc_p_97
    main['ERC_99th_percentile'] = erc_p_99

    if os.path.exists(f"FEMS Data/{gacc_region}"):
        pass
    else:
        os.mkdir(f"FEMS Data/{gacc_region}")
    
    if os.path.exists(f"FEMS Data/{gacc_region}/PSA Percentiles"):
        pass
    else:
        os.mkdir(f"FEMS Data/{gacc_region}/PSA Percentiles")
    
    fname = f"PSA_Percentiles.csv"
    main.to_csv(fname, index=False)
    os.replace(f"{fname}", f"FEMS Data/{gacc_region}/PSA Percentiles/{fname}")


def sort_data_by_zone(gacc_region):

    gacc_region = gacc_region.upper()
    
    try:
        now = datetime.now(UTC)
    except Exception as e:
        now = datetime.utcnow()

    last_year = now.year - 1

    if now.month >= 11:
        start_date = datetime(now.year, 11, 1)
    else:
        start_date = datetime(last_year, 11, 1)
    end_date = datetime(now.year, now.month, now.day)
    
    paths = []
    for folder in os.listdir(f"FEMS Data/Stations/{gacc_region}"):
        path = f"FEMS Data/Stations/{gacc_region}/{folder}"
        paths.append(path)
    
    psa = 1
    for p in range(0, len(paths)):
        files = []
        for file in os.listdir(paths[p]):
            files.append(file)
    
        dates = []
        
        dfm_100 = []
        dfm_100hr_mean = []
        dfm_100hr_min = []
        dfm_100hr_max = []
        
        dfm_1000 = []
        dfm_1000hr_mean = []
        dfm_1000hr_min = []
        dfm_1000hr_max = []
    
        erc = []
        erc_mean = []
        erc_min = []
        erc_max = []
        
        for i in range(0, len(files)):
            try:
                df = pd.read_csv(f"{paths[p]}/{files[i]}")
                df = df[df['observationTime'].between(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))]
                dfm_100.append(df['hundredHR_TL_FuelMoisture'])
                dates.append(df['observationTime'])
                dfm_1000.append(df['thousandHR_TL_FuelMoisture'])
                erc.append(df['energyReleaseComponent'])
                
            except Exception as e:
                pass
    
        try:
            df_dates = pd.DataFrame(dates)
        except Exception as e:
            pass
    
        try:
            df_100 = pd.DataFrame(dfm_100)
            df_100 = df_100.transpose()
            for i in range(0, len(df_100)):
                mean = np.nanmean(df_100.iloc[i])
                dfm_100hr_mean.append(mean)
        except Exception as e:
            pass
    
        try:
            for i in range(0, len(df_100)):
                minimum = np.nanmin(df_100.iloc[i])
                dfm_100hr_min.append(minimum)
        except Exception as e:
            pass        
    
        try:
            for i in range(0, len(df_100)):
                maximum = np.nanmax(df_100.iloc[i])
                dfm_100hr_max.append(maximum)
        except Exception as e:
            pass    
    
        try:
            df_1000 = pd.DataFrame(dfm_1000)
            df_1000 = df_1000.transpose()
            for i in range(0, len(df_1000)):
                mean = np.nanmean(df_1000.iloc[i])
                dfm_1000hr_mean.append(mean)
        except Exception as e:
            pass
    
        try:
            for i in range(0, len(df_1000)):
                minimum = np.nanmin(df_1000.iloc[i])
                dfm_1000hr_min.append(minimum)
        except Exception as e:
            pass        
    
        try:
            for i in range(0, len(df_1000)):
                maximum = np.nanmax(df_1000.iloc[i])
                dfm_1000hr_max.append(maximum)
        except Exception as e:
            pass    
    
        try:
            df_erc = pd.DataFrame(erc)
            df_erc = df_erc.transpose()
            for i in range(0, len(df_erc)):
                mean = np.nanmean(df_erc.iloc[i])
                erc_mean.append(mean)
        except Exception as e:
            pass
    
        try:
            for i in range(0, len(df_erc)):
                minimum = np.nanmin(df_erc.iloc[i])
                erc_min.append(minimum)
        except Exception as e:
            pass        
    
        try:
            for i in range(0, len(df_erc)):
                maximum = np.nanmax(df_erc.iloc[i])
                erc_max.append(maximum)
        except Exception as e:
            pass    
    
        main = pd.DataFrame()
        
        main['date'] = df_dates.iloc[0]
        
        main['100hr_DFM_mean'] = dfm_100hr_mean
        main['100hr_DFM_min'] = dfm_100hr_min
        main['100hr_DFM_max'] = dfm_100hr_max
    
        main['1000hr_DFM_mean'] = dfm_1000hr_mean
        main['1000hr_DFM_min'] = dfm_1000hr_min
        main['1000hr_DFM_max'] = dfm_1000hr_max
    
        main['ERC_mean'] = erc_mean
        main['ERC_min'] = erc_min
        main['ERC_max'] = erc_max
    
        if os.path.exists(f"FEMS Data/{gacc_region}/PSA Data"):
            pass
        else:
            os.mkdir(f"FEMS Data/{gacc_region}/PSA Data")
        
        fname = f"zone_{psa}.csv"
        main.to_csv(fname, index=False)
        os.replace(f"{fname}", f"FEMS Data/{gacc_region}/PSA Data/{fname}")
        psa = psa + 1























