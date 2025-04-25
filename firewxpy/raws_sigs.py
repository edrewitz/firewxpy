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
import shutil

from datetime import datetime, timedelta
from calendar import isleap

def get_number_of_psas_by_gacc(gacc_region):

    gacc_region = gacc_region.upper()

    if gacc_region == 'OSCC':
        psas = 17
    if gacc_region == 'ONCC':
        psas = 9
    if gacc_region == 'AICC':
        psas = 19
    if gacc_region == 'NWCC':
        psas = 13
    if gacc_region == 'NRCC':
        psas = 14
    if gacc_region == 'GBCC':
        psas = 36
    if gacc_region == 'SWCC':
        psas = 16
    if gacc_region == 'RMCC':
        psas = 29
    if gacc_region == 'SACC':
        psas = 57
    if gacc_region == 'EACC':
        psas = 25

    return psas

def calculate_daily_stats(df):
    """Calculate daily max, min and average statistics for the selected component."""
    daily_max = df.groupby('julian_date').max(numeric_only=True).reset_index()
    daily_min = df.groupby('julian_date').min(numeric_only=True).reset_index()
    daily_avg = df.groupby('julian_date').mean(numeric_only=True).reset_index()
    return daily_max, daily_min, daily_avg

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

def get_stats(gacc_region):

    gacc_region = gacc_region.upper()
    
    paths = []
    
    if os.path.exists(f"FEMS Data/Station Climo"):
        pass
    else:
        os.mkdir(f"FEMS Data/Station Climo")

    if os.path.exists(f"FEMS Data/Station Climo/{gacc_region}"):
        pass
    else:
        os.mkdir(f"FEMS Data/Station Climo/{gacc_region}")
    
    psa = 1
    for folder in os.listdir(f"FEMS Data/Stations/{gacc_region}"):
        path = f"FEMS Data/Stations/{gacc_region}/{folder}"
        paths.append(path) 
    
        if os.path.exists(f"FEMS Data/Station Climo/{gacc_region}/PSA {psa}"):
            pass
        else:
            os.mkdir(f"FEMS Data/Station Climo/{gacc_region}/PSA {psa}")
    
        if os.path.exists(f"FEMS Data/Station Climo/{gacc_region}/PSA {psa}/MAX"):
            pass
        else:
            os.mkdir(f"FEMS Data/Station Climo/{gacc_region}/PSA {psa}/MAX")   
    
        if os.path.exists(f"FEMS Data/Station Climo/{gacc_region}/PSA {psa}/MIN"):
            pass
        else:
            os.mkdir(f"FEMS Data/Station Climo/{gacc_region}/PSA {psa}/MIN")   
    
        if os.path.exists(f"FEMS Data/Station Climo/{gacc_region}/PSA {psa}/AVG"):
            pass
        else:
            os.mkdir(f"FEMS Data/Station Climo/{gacc_region}/PSA {psa}/AVG")   
    
        max_vals = []
        mean_vals = []
        min_vals = []
    
        for p in range(0, len(paths)):
            files = []
        if os.path.exists(f"{paths[p]}/.ipynb_checkpoints"):
            shutil.rmtree(f"{paths[p]}/.ipynb_checkpoints")
        else:
            pass
            for file in os.listdir(paths[p]):
                files.append(file)  
                
        for i in range(0, len(files)):
    
            df = pd.read_csv(f"{paths[p]}/{files[i]}")
            daily_max = df.groupby('julian_date').max(numeric_only=True)
            daily_min = df.groupby('julian_date').min(numeric_only=True)
            daily_avg = df.groupby('julian_date').mean(numeric_only=True)
    
            fname_max = f"{df['stationId'].iloc[0]}_max.csv"
            fname_min = f"{df['stationId'].iloc[0]}_min.csv"
            fname_avg = f"{df['stationId'].iloc[0]}_avg.csv"
            daily_max.to_csv(fname_max, index=False)
            os.replace(f"{fname_max}", f"FEMS Data/Station Climo/{gacc_region}/PSA {psa}/MAX/{fname_max}")
            daily_min.to_csv(fname_min, index=False)
            os.replace(f"{fname_min}", f"FEMS Data/Station Climo/{gacc_region}/PSA {psa}/MIN/{fname_min}")
            daily_avg.to_csv(fname_avg, index=False)
            os.replace(f"{fname_avg}", f"FEMS Data/Station Climo/{gacc_region}/PSA {psa}/AVG/{fname_avg}")
        psa = psa + 1

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
                df['observationTime'] = pd.to_datetime(df['observationTime'])
                
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

def station_stats(gacc_region):

    gacc_region = gacc_region.upper()
    
    try:
        now = datetime.now(UTC)
    except Exception as e:
        now = datetime.utcnow()

    start_date = datetime(now.year, 1, 1)
    end_date = datetime(now.year, now.month, now.day)
    
    paths = []
    for folder in os.listdir(f"FEMS Data/Stations/{gacc_region}"):
        path = f"FEMS Data/Stations/{gacc_region}/{folder}"
        paths.append(path)
    
    psa = 1
    
    if os.path.exists(f"FEMS Data/Station Stats"):
        pass
    else:
        os.mkdir(f"FEMS Data/Station Stats")
    
    if os.path.exists(f"FEMS Data/Station Stats/{gacc_region}"):
        pass
    else:
        os.mkdir(f"FEMS Data/Station Stats/{gacc_region}")
    
    for p in range(0, len(paths)):
        files = []
        
        if os.path.exists(f"{paths[p]}/.ipynb_checkpoints"):
            shutil.rmtree(f"{paths[p]}/.ipynb_checkpoints")
        else:
            pass
            
        for file in os.listdir(paths[p]):
            files.append(file)
    
        if os.path.exists(f"FEMS Data/Station Stats/{gacc_region}/PSA {psa}"):
            pass
        else:
            os.mkdir(f"FEMS Data/Station Stats/{gacc_region}/PSA {psa}")
    
        days = abs((start_date - end_date).days)
        dates = []
        for day in range(0, days):
            date = start_date + timedelta(days=day)
            dates.append(date)
        
        for i in range(0, len(files)):
    
            df = pd.read_csv(f"{paths[p]}/{files[i]}")
            df = df[df['observationTime'].between(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))]
            df['observationTime'] = pd.to_datetime(df['observationTime'])
            df['julian_date'] = df['observationTime'].dt.dayofyear
            data = df.groupby(pd.Grouper(key='observationTime', freq='D'))
            f100 = data['hundredHR_TL_FuelMoisture'].min()
            f1000 = data['thousandHR_TL_FuelMoisture'].min()
            erc = data['energyReleaseComponent'].max()
            bi = data['burningIndex'].max()
            sc = data['spreadComponent'].max()
    
            if len(f100) == days and len(f1000) == days and len(erc) == days and len(bi) == days and len(sc) == days:
                main = pd.DataFrame()
                main['f100'] = f100.values
                main['f1000'] = f1000.values
                main['erc'] = erc.values
                main['bi'] = bi.values
                main['sc'] = sc.values
                main['dates'] = dates
        
                fname = f"{files[i]}"
                main.to_csv(fname, index=False)
                os.replace(f"{fname}", f"FEMS Data/Station Stats/{gacc_region}/PSA {psa}/{fname}")
            else:
                pass
    
        psa = psa + 1

def sort_data_by_psa(gacc_region):

    gacc_region = gacc_region.upper()
    
    paths = []
    for folder in os.listdir(f"FEMS Data/Station Stats/{gacc_region}"):
        path = f"FEMS Data/Station Stats/{gacc_region}/{folder}"
        paths.append(path)
    
    psa = 1
    for p in range(0, len(paths)):
        files = []
        
        if os.path.exists(f"{paths[p]}/.ipynb_checkpoints"):
            shutil.rmtree(f"{paths[p]}/.ipynb_checkpoints")
        else:
            pass
            
        for file in os.listdir(paths[p]):
            files.append(file)    
    
        dates = []
    
        f100 = []
        f100_max = []
        f100_min = []
        f100_mean = []
    
        f1000 = []
        f1000_max = []
        f1000_min = []
        f1000_mean = []
    
        erc = []
        erc_max = []
        erc_min = []
        erc_mean = []
    
        bi = []
        bi_max = []
        bi_min = []
        bi_mean = []
    
        sc = []
        sc_max = []
        sc_min = []
        sc_mean = []
    
        d = pd.read_csv(f"{paths[p]}/{files[0]}")
        dates.append(d['dates'])
        
        for i in range(0, len(files)):
            try:
                df = pd.read_csv(f"{paths[p]}/{files[i]}")
                f100.append(df['f100'])
                f1000.append(df['f1000'])
                erc.append(df['erc'])
                bi.append(df['bi'])
                sc.append(df['sc'])
            except Exception as e:
                pass
                         
            
        try:
            df_dates = pd.DataFrame(dates)
            df_dates = df_dates.transpose()
        except Exception as e:
            pass    
    
        try:
            df_100 = pd.DataFrame(f100)
            df_100 = df_100.transpose()
            for i in range(0, len(df_100)):
                mean_100 = df_100.iloc[i].mean()
                maxima_100 = df_100.iloc[i].max()
                minima_100 = df_100.iloc[i].min()
                f100_mean.append(mean_100)
                f100_max.append(maxima_100)
                f100_min.append(minima_100)
        except Exception as e:
            pass    
    
        try:
            df_1000 = pd.DataFrame(f1000)
            df_1000 = df_1000.transpose()
            for i in range(0, len(df_1000)):
                mean_1000 = df_1000.iloc[i].mean()
                maxima_1000 = df_1000.iloc[i].max()
                minima_1000 = df_1000.iloc[i].min()
                f1000_mean.append(mean_1000)
                f1000_max.append(maxima_1000)
                f1000_min.append(minima_1000)
        except Exception as e:
            pass  
    
        try:
            df_erc = pd.DataFrame(erc)
            df_erc = df_erc.transpose()
            for i in range(0, len(df_erc)):
                mean_erc = df_erc.iloc[i].mean()
                maxima_erc = df_erc.iloc[i].max()
                minima_erc = df_erc.iloc[i].min()
                erc_mean.append(mean_erc)
                erc_max.append(maxima_erc)
                erc_min.append(minima_erc)
        except Exception as e:
            pass  
    
        try:
            df_bi = pd.DataFrame(bi)
            df_bi = df_bi.transpose()
            for i in range(0, len(df_bi)):
                mean_bi = df_bi.iloc[i].mean()
                maxima_bi = df_bi.iloc[i].max()
                minima_bi = df_bi.iloc[i].min()
                bi_mean.append(mean_bi)
                bi_max.append(maxima_bi)
                bi_min.append(minima_bi)
        except Exception as e:
            pass  
    
        try:
            df_sc = pd.DataFrame(sc)
            df_sc = df_sc.transpose()
            for i in range(0, len(df_sc)):
                mean_sc = df_sc.iloc[i].mean()
                maxima_sc = df_sc.iloc[i].max()
                minima_sc = df_sc.iloc[i].min()
                sc_mean.append(mean_sc)
                sc_max.append(maxima_sc)
                sc_min.append(minima_sc)
        except Exception as e:
            pass  
    
        main = pd.DataFrame()
        
        main['dates'] = df_dates
        main['dates'] = pd.to_datetime(main['dates'])
        main['julian_date'] = main['dates'].dt.dayofyear
        
        main['f100_mean'] = f100_mean
        main['f100_max'] = f100_max
        main['f100_min'] = f100_min
        
        main['f1000_mean'] = f1000_mean
        main['f1000_max'] = f1000_max
        main['f1000_min'] = f1000_min
        
        main['erc_mean'] = erc_mean
        main['erc_max'] = erc_max
        main['erc_min'] = erc_min
        
        main['bi_mean'] = bi_mean
        main['bi_max'] = bi_max
        main['bi_min'] = bi_min
        
        main['sc_mean'] = sc_mean
        main['sc_max'] = sc_max
        main['sc_min'] = sc_min
    
        if os.path.exists(f"FEMS Data/{gacc_region}/PSA Data"):
            pass
        else:
            os.mkdir(f"FEMS Data/{gacc_region}/PSA Data")
        
        fname = f"zone_{psa}.csv"
        main.to_csv(fname, index=False)
        os.replace(f"{fname}", f"FEMS Data/{gacc_region}/PSA Data/{fname}")
        psa = psa + 1

def get_psa_climatology(gacc_region):
    
    num_psas = get_number_of_psas_by_gacc(gacc_region)
    
    gacc_region = gacc_region.upper()
    
    for psa in range(1, num_psas):
        paths = []
        for folder in os.listdir(f"FEMS Data/Station Climo/{gacc_region}/PSA {psa}"):
            path = f"FEMS Data/Station Climo/{gacc_region}/PSA {psa}/{folder}"
            paths.append(path)
    
        for p in range(0, len(paths)):
            files = []
            
            if os.path.exists(f"{paths[p]}/.ipynb_checkpoints"):
                shutil.rmtree(f"{paths[p]}/.ipynb_checkpoints")
            else:
                pass
                
            for file in os.listdir(paths[p]):
                files.append(file)
    
                f100 = []
                f1000 = []
                erc = []
                bi = []
                sc = []
    
                for i in range(0, len(files)):
                    try:
                        df = pd.read_csv(f"{paths[p]}/{files[i]}")
                        f100.append(df['hundredHR_TL_FuelMoisture'])
                        f1000.append(df['thousandHR_TL_FuelMoisture'])
                        erc.append(df['energyReleaseComponent'])
                        bi.append(df['burningIndex'])
                        sc.append(df['spreadComponent'])
                    except Exception as e:
                        pass
    
                f100_vals = pd.DataFrame()
                for i in range(0, len(f100)):
                    f100_vals[f'col{i}'] = f100[i]
    
                f1000_vals = pd.DataFrame()
                for i in range(0, len(f1000)):
                    f1000_vals[f'col{i}'] = f1000[i]
    
                erc_vals = pd.DataFrame()
                for i in range(0, len(erc)):
                    erc_vals[f'col{i}'] = erc[i]
    
                bi_vals = pd.DataFrame()
                for i in range(0, len(bi)):
                    bi_vals[f'col{i}'] = bi[i]    
    
                sc_vals = pd.DataFrame()
                for i in range(0, len(sc)):
                    sc_vals[f'col{i}'] = sc[i]    

                f100_vals['min'] = f100_vals.min(axis=1, numeric_only=True, skipna=True)
                f100_vals['avg'] = f100_vals.mean(axis=1, numeric_only=True, skipna=True)
                
                f1000_vals['min'] = f1000_vals.min(axis=1, numeric_only=True, skipna=True)
                f1000_vals['avg'] = f1000_vals.mean(axis=1, numeric_only=True, skipna=True)
    
                erc_vals['max'] = erc_vals.max(axis=1, numeric_only=True, skipna=True)
                erc_vals['avg'] = erc_vals.mean(axis=1, numeric_only=True, skipna=True)
    
                bi_vals['max'] = bi_vals.max(axis=1, numeric_only=True, skipna=True)
                bi_vals['avg'] = bi_vals.mean(axis=1, numeric_only=True, skipna=True)
    
                sc_vals['max'] = sc_vals.max(axis=1, numeric_only=True, skipna=True)
                sc_vals['avg'] = sc_vals.mean(axis=1, numeric_only=True, skipna=True)
    
            main = pd.DataFrame()
    
            main['f100_min'] = f100_vals['min']
            main['f100_avg'] = f100_vals['avg']
            main['f1000_min'] = f1000_vals['min']
            main['f1000_avg'] = f1000_vals['avg']
            main['erc_max'] = erc_vals['max']
            main['erc_avg'] = erc_vals['avg']
            main['bi_max'] = bi_vals['max']
            main['bi_avg'] = bi_vals['avg']
            main['sc_max'] = sc_vals['max']
            main['sc_avg'] = sc_vals['avg']
            jdate = np.arange(1, 367, 1)
            main['julian_date'] = jdate

            if p == 0:
                folder_name = 'AVG'
            if p == 1:
                folder_name = 'MAX'
            if p == 2:
                folder_name = 'MIN'
    
            if os.path.exists(f"FEMS Data/{gacc_region}/PSA Climo"):
                pass
            else:
                os.mkdir(f"FEMS Data/{gacc_region}/PSA Climo")

            if os.path.exists(f"FEMS Data/{gacc_region}/PSA Climo/{folder_name}"):
                pass
            else:
                os.mkdir(f"FEMS Data/{gacc_region}/PSA Climo/{folder_name}")
            
            fname = f"zone_{psa}.csv"
            main.to_csv(fname, index=False)
            os.replace(f"{fname}", f"FEMS Data/{gacc_region}/PSA Climo/{folder_name}/{fname}")
