
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as md
import os
import pandas as pd
import shutil
import numpy as np

from firewxpy.data_access import FEMS
from firewxpy.raws_sigs import get_psa_percentiles, station_stats, sort_data_by_psa, get_stats, get_psa_climatology, station_forecast, sort_forecasts_by_psa
from firewxpy.standard import plot_creation_time, get_timezone_abbreviation, get_timezone
try:
    from datetime import datetime, timedelta, UTC
except Exception as e:
    from datetime import datetime, timedelta
from firewxpy.utilities import file_functions
from calendar import isleap

local_time, utc_time = plot_creation_time()
timezone = get_timezone_abbreviation()
tzone = get_timezone()

mpl.rcParams['font.weight'] = 'bold'
props = dict(boxstyle='round', facecolor='wheat', alpha=1)
date_box = dict(boxstyle='round', facecolor='dimgrey', alpha=1)

mpl.rcParams['xtick.labelsize'] = 9
mpl.rcParams['ytick.labelsize'] = 9

plt.style.use("ggplot")

def get_psa_ids(gacc_region):

    gacc_region = gacc_region.upper()

    if gacc_region == "SACC":
        psaIDs = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12",
                  "13",
                  "14",
                  "15",
                  "16",
                  "17A",
                  "17B",
                  "18",
                  "19",
                  "20",
                  "21A",
                  "21B",
                  "21C",
                  "22A",
                  "22B",
                  "23",
                  "24",
                  "25",
                  "25B",
                  "26",
                  "27",
                  "28A",
                  "28B",
                  "29",
                  "30",
                  "31A",
                  "31B",
                  "31C",
                  "32",
                  "33",
                  "34",
                  "35",
                  "36",
                  "37",
                  "38",
                  "39",
                  "40",
                  "41",
                  "42",
                  "46",
                  "47",
                  "48",
                  "49",
                  "50",
                  "52"
                 ]

    if gacc_region == 'ONCC':
        psaIDs = ["1",
                  "2",
                  "3A",
                  "3B",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8"
                 ]

    if gacc_region == "OSCC":
        psaIDs = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12",
                  "13",
                  "14",
                  "15",
                  "16"
                 ]

    if gacc_region == "GBCC":
        psaIDs = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12",
                  "13",
                  "14",
                  "15",
                  "16",
                  "17",
                  "18",
                  "19",
                  "20",
                  "21",
                  "22",
                  "23",
                  "24",
                  "25",
                  "26",
                  "27",
                  "28",
                  "29",
                  "30",
                  "31",
                  "32",
                  "33",
                  "34",
                  "35"                  
                 ]

    if gacc_region == "EACC":
        psaIDs = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12",
                  "13",
                  "14",
                  "15",
                  "16",
                  "17",
                  "18",
                  "19",
                  "20",
                  "21",
                  "22",
                  "23",
                  "24"
                 ]


    if gacc_region == "NRCC":
        psaIDs = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12",
                  "13",
                  "14",
                  "15",
                  "16",
                  "17",
                  "18"
                 ]

    if gacc_region == "NWCC":
        psaIDs = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12"
                 ]

    if gacc_region == "RMCC":
        psaIDs = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12",
                  "13",
                  "14",
                  "15",
                  "16",
                  "17",
                  "18",
                  "19",
                  "20",
                  "21",
                  "22",
                  "23",
                  "24",
                  "25",
                  "26",
                  "27",
                  "28"
                 ]

    if gacc_region == "SWCC":
        psaIDs = ["1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6N",
                  "6S",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12",
                  "13",
                  "14N"
                 ]
                  
    return psaIDs                 
    

def create_psa_100hr_fuels_charts(gacc_region, number_of_years_for_averages=15, fuel_model='Y', start_date=None, data=False):
    
    gacc_region = gacc_region.upper()

    path, path_print = file_functions.get_fuels_charts_paths(gacc_region, '100hr Dead Fuel')

    if data == False:
        FEMS.get_raws_sig_data(gacc_region, number_of_years_for_averages, fuel_model, start_date)
        FEMS.get_nfdrs_forecast_data(gacc_region, fuel_model)
    else:
        pass
        
    get_psa_percentiles(gacc_region)
    station_stats(gacc_region)
    get_stats(gacc_region)
    get_psa_climatology(gacc_region)
    sort_data_by_psa(gacc_region)
    station_forecast(gacc_region)
    sort_forecasts_by_psa(gacc_region)

    data_dir = f"FEMS Data/{gacc_region}/PSA Data"
    percentiles_dir = f"FEMS Data/{gacc_region}/PSA Percentiles"
    climo_avg_dir = f"FEMS Data/{gacc_region}/PSA Climo/AVG"
    climo_min_dir = f"FEMS Data/{gacc_region}/PSA Climo/MIN"
    forecast_dir = f"FEMS Data/{gacc_region}/PSA Forecast"

    percentiles = pd.read_csv(f"FEMS Data/{gacc_region}/PSA Percentiles/PSA_Percentiles.csv")

    leap = isleap(utc_time.year)
    if start_date == None:
        if leap == False:
            days = number_of_years_for_averages * 365
        else:
            days = number_of_years_for_averages * 366
        start_date = utc_time - timedelta(days=days)
        start_year = start_date.year
        xmin = start_date
        xmax = utc_time

    else:
        start_date = start_date
        start_year = f"{start_date[0]}{start_date[1]}{start_date[2]}{start_date[3]}"
        start_month = f"{start_date[5]}{start_date[6]}"
        start_day = f"{start_date[8]}{start_date[9]}"
        xmin = datetime(int(start_year), int(start_month), int(start_day))
        xmax = utc_time
    
    psa = 1

    if os.path.exists(f"{data_dir}/.ipynb_checkpoints"):
        shutil.rmtree(f"{data_dir}/.ipynb_checkpoints")
    else:
        pass

    if os.path.exists(f"{data_dir}/.ipynb_checkpoints"):
        shutil.rmtree(f"{data_dir}/.ipynb_checkpoints")
    else:
        pass

    files = os.listdir(f"{data_dir}")
    psa = 1

    psa_IDs = get_psa_ids(gacc_region)              
              
              
    for i in range(0, len(files)):

        fname = f"{psa_IDs[i]}.png"
        psaID = psa_IDs[i]

        try:
            df_data = pd.read_csv(f"{data_dir}/zone_{psa}.csv") 
            try:
                df_forecast = pd.read_csv(f"{forecast_dir}/zone_{psa}.csv") 
            except Exception as e:
                pass
            df_climo_avg = pd.read_csv(f"{climo_avg_dir}/zone_{psa}.csv") 
            df_climo_min = pd.read_csv(f"{climo_min_dir}/zone_{psa}.csv") 
        except Exception as e:
            pass

        try:
            dates = pd.to_datetime(df_data['dates'])
        except Exception as e:
            pass

        fig = plt.figure(figsize=(12,12))

        ax = fig.add_subplot(1, 1, 1)

        ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
        plt.title(f"100-HR Dead Fuel Moisture: {gacc_region} PSA {psaID}", fontsize=12, fontweight='bold', loc='left')
        plt.title(f"Period Of Record: {start_year} - {utc_time.year}", fontsize=10, fontweight='bold', loc='right')
        ax.text(0.01, -0.05, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: USDA/FEMS", transform=ax.transAxes, fontsize=8, fontweight='bold', bbox=props)
        ax.text(0.65, -0.05, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=7, fontweight='bold', bbox=props)
        ax.text(0.405, 0.98, f"Valid Date: {dates.iloc[-1].strftime("%m/%d/%Y")}", transform=ax.transAxes, fontsize=8, color='white', fontweight='bold', bbox=date_box)

        if leap == True:
            jmax = 366
        else:
            jmax = 365
        
        ax.set_xlim(0, jmax)

        try:
            data_max = np.nanmax(df_data['f100_mean'])
            try:
                forecast_max = np.nanmax(df_forecast['f100_mean'])
                if data_max >= forecast_max:
                    max_bound = data_max
                else:
                    max_bound = forecast_max
            except Exception as e:
                max_bound = data_max
    
            max_bound = max_bound + 10
        except Exception as e:
            max_bound = 30
            
        ax.set_ylim(0, max_bound)

        try:
            ax.hlines(percentiles['100hr_DFM_3_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='-', alpha=0.5, zorder=2, label=f"3RD PERCENTILE")
            ax.hlines(percentiles['100hr_DFM_10_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='--', alpha=0.5, zorder=2, label=f"10TH PERCENTILE")
            ax.hlines(percentiles['100hr_DFM_20_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='-.', alpha=0.5, zorder=2, label=f"20TH PERCENTILE")
            ax.hlines(percentiles['100hr_DFM_40_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle=':', alpha=0.5, zorder=2, label=f"40TH PERCENTILE")
    
            ax.axhspan(0, percentiles['100hr_DFM_3_percentile'].iloc[i], color='saddlebrown', alpha=0.2, label=f"0TH-3RD PERCENTILE")
            ax.axhspan(percentiles['100hr_DFM_3_percentile'].iloc[i], percentiles['100hr_DFM_10_percentile'].iloc[i], color='peru', alpha=0.2, label=f"3RD-10TH PERCENTILE")
            ax.axhspan(percentiles['100hr_DFM_10_percentile'].iloc[i], percentiles['100hr_DFM_20_percentile'].iloc[i], color='orange', alpha=0.2, label=f"10TH-20TH PERCENTILE")
            ax.axhspan(percentiles['100hr_DFM_20_percentile'].iloc[i], percentiles['100hr_DFM_40_percentile'].iloc[i], color='gold', alpha=0.2, label=f"20TH-40TH PERCENTILE")
            ax.axhspan(percentiles['100hr_DFM_40_percentile'].iloc[i], max_bound, color='lime', alpha=0.2, label=f"40TH-100TH PERCENTILE")
    
            ax.plot(df_data['julian_date'], df_data['f100_mean'], color='blue', alpha=1, label=f"OBSERVED")
            ax.plot(df_climo_avg['julian_date'], df_climo_avg['f100_avg'], color='gray', alpha=1, label=f"AVERAGE")
            ax.plot(df_climo_min['julian_date'], df_climo_min['f100_min'], color='red', alpha=1, label=f"MAX")
    
            try:
               ax.plot([df_data['julian_date'].iloc[-1], df_forecast['julian_date'].iloc[0]], [df_data['f100_mean'].iloc[-1], df_forecast['f100_mean'].iloc[0]], color='green', alpha=1)  
               ax.plot(df_forecast['julian_date'], df_forecast['f100_mean'], color='green', alpha=1, label=f"FORECAST") 
            except Exception as e:
                pass
    
            
            plt.legend(loc="upper left", fontsize="xx-small")
        except Exception as e:
            pass

        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        psa = psa + 1

    print(f"100-HR Fuels Charts Saved To {path_print}")

        
def create_psa_1000hr_fuels_charts(gacc_region, number_of_years_for_averages=15, fuel_model='Y', start_date=None, data=False):
    
    gacc_region = gacc_region.upper()

    path, path_print = file_functions.get_fuels_charts_paths(gacc_region, '1000hr Dead Fuel')

    if data == False:
        FEMS.get_raws_sig_data(gacc_region, number_of_years_for_averages, fuel_model, start_date)
        FEMS.get_nfdrs_forecast_data(gacc_region, fuel_model)
    else:
        pass
        
    get_psa_percentiles(gacc_region)
    station_stats(gacc_region)
    get_stats(gacc_region)
    get_psa_climatology(gacc_region)
    sort_data_by_psa(gacc_region)
    station_forecast(gacc_region)
    sort_forecasts_by_psa(gacc_region)

    data_dir = f"FEMS Data/{gacc_region}/PSA Data"
    percentiles_dir = f"FEMS Data/{gacc_region}/PSA Percentiles"
    climo_avg_dir = f"FEMS Data/{gacc_region}/PSA Climo/AVG"
    climo_min_dir = f"FEMS Data/{gacc_region}/PSA Climo/MIN"
    forecast_dir = f"FEMS Data/{gacc_region}/PSA Forecast"

    percentiles = pd.read_csv(f"FEMS Data/{gacc_region}/PSA Percentiles/PSA_Percentiles.csv")

    leap = isleap(utc_time.year)
    if start_date == None:
        if leap == False:
            days = number_of_years_for_averages * 365
        else:
            days = number_of_years_for_averages * 366
        start_date = utc_time - timedelta(days=days)
        start_year = start_date.year
        xmin = start_date
        xmax = utc_time

    else:
        start_date = start_date
        start_year = f"{start_date[0]}{start_date[1]}{start_date[2]}{start_date[3]}"
        start_month = f"{start_date[5]}{start_date[6]}"
        start_day = f"{start_date[8]}{start_date[9]}"
        xmin = datetime(int(start_year), int(start_month), int(start_day))
        xmax = utc_time
    
    psa = 1

    if os.path.exists(f"{data_dir}/.ipynb_checkpoints"):
        shutil.rmtree(f"{data_dir}/.ipynb_checkpoints")
    else:
        pass

    if os.path.exists(f"{data_dir}/.ipynb_checkpoints"):
        shutil.rmtree(f"{data_dir}/.ipynb_checkpoints")
    else:
        pass

    files = os.listdir(f"{data_dir}")
    psa = 1

    psa_IDs = get_psa_ids(gacc_region)              
              
    for i in range(0, len(files)):

        fname = f"{psa_IDs[i]}.png"
        psaID = psa_IDs[i]

        try:
            df_data = pd.read_csv(f"{data_dir}/zone_{psa}.csv") 
            try:
                df_forecast = pd.read_csv(f"{forecast_dir}/zone_{psa}.csv") 
            except Exception as e:
                pass
            df_climo_avg = pd.read_csv(f"{climo_avg_dir}/zone_{psa}.csv") 
            df_climo_min = pd.read_csv(f"{climo_min_dir}/zone_{psa}.csv") 
        except Exception as e:
            pass

        try:
            dates = pd.to_datetime(df_data['dates'])
        except Exception as e:
            pass

        fig = plt.figure(figsize=(12,12))

        ax = fig.add_subplot(1, 1, 1)

        ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
        plt.title(f"1000-HR Dead Fuel Moisture: {gacc_region} PSA {psaID}", fontsize=12, fontweight='bold', loc='left')
        plt.title(f"Period Of Record: {start_year} - {utc_time.year}", fontsize=10, fontweight='bold', loc='right')
        ax.text(0.01, -0.05, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: USDA/FEMS", transform=ax.transAxes, fontsize=8, fontweight='bold', bbox=props)
        ax.text(0.65, -0.05, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=7, fontweight='bold', bbox=props)
        ax.text(0.405, 0.98, f"Valid Date: {dates.iloc[-1].strftime("%m/%d/%Y")}", transform=ax.transAxes, fontsize=8, color='white', fontweight='bold', bbox=date_box)

        if leap == True:
            jmax = 366
        else:
            jmax = 365
        
        ax.set_xlim(0, jmax)

        try:
            data_max = np.nanmax(df_data['f1000_mean'])
            try:
                forecast_max = np.nanmax(df_forecast['f1000_mean'])
                if data_max >= forecast_max:
                    max_bound = data_max
                else:
                    max_bound = forecast_max
            except Exception as e:
                max_bound = data_max
    
            max_bound = max_bound + 10
        except Exception as e:
            max_bound = 30
            
        ax.set_ylim(0, max_bound)

        try:
            ax.hlines(percentiles['1000hr_DFM_3_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='-', alpha=0.5, zorder=2, label=f"3RD PERCENTILE")
            ax.hlines(percentiles['1000hr_DFM_10_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='--', alpha=0.5, zorder=2, label=f"10TH PERCENTILE")
            ax.hlines(percentiles['1000hr_DFM_20_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='-.', alpha=0.5, zorder=2, label=f"20TH PERCENTILE")
            ax.hlines(percentiles['1000hr_DFM_40_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle=':', alpha=0.5, zorder=2, label=f"40TH PERCENTILE")
    
            ax.axhspan(0, percentiles['1000hr_DFM_3_percentile'].iloc[i], color='saddlebrown', alpha=0.2, label=f"0TH-3RD PERCENTILE")
            ax.axhspan(percentiles['1000hr_DFM_3_percentile'].iloc[i], percentiles['1000hr_DFM_10_percentile'].iloc[i], color='peru', alpha=0.2, label=f"3RD-10TH PERCENTILE")
            ax.axhspan(percentiles['1000hr_DFM_10_percentile'].iloc[i], percentiles['1000hr_DFM_20_percentile'].iloc[i], color='orange', alpha=0.2, label=f"10TH-20TH PERCENTILE")
            ax.axhspan(percentiles['1000hr_DFM_20_percentile'].iloc[i], percentiles['1000hr_DFM_40_percentile'].iloc[i], color='gold', alpha=0.2, label=f"20TH-40TH PERCENTILE")
            ax.axhspan(percentiles['1000hr_DFM_40_percentile'].iloc[i], max_bound, color='lime', alpha=0.2, label=f"40TH-100TH PERCENTILE")
    
            ax.plot(df_data['julian_date'], df_data['f1000_mean'], color='blue', alpha=1, label=f"OBSERVED")
            ax.plot(df_climo_avg['julian_date'], df_climo_avg['f1000_avg'], color='gray', alpha=1, label=f"AVERAGE")
            ax.plot(df_climo_min['julian_date'], df_climo_min['f1000_min'], color='red', alpha=1, label=f"MAX")
    
            try:
               ax.plot([df_data['julian_date'].iloc[-1], df_forecast['julian_date'].iloc[0]], [df_data['f1000_mean'].iloc[-1], df_forecast['f1000_mean'].iloc[0]], color='green', alpha=1)  
               ax.plot(df_forecast['julian_date'], df_forecast['f1000_mean'], color='green', alpha=1, label=f"FORECAST") 
            except Exception as e:
                pass
    
            
            plt.legend(loc="upper left", fontsize="xx-small")
        except Exception as e:
            pass

        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        psa = psa + 1

    print(f"1000-HR Fuels Charts Saved To {path_print}")



def create_psa_erc_fuels_charts(gacc_region, number_of_years_for_averages=15, fuel_model='Y', start_date=None, data=False):
    
    gacc_region = gacc_region.upper()

    path, path_print = file_functions.get_fuels_charts_paths(gacc_region, 'ERC')

    if data == False:
        FEMS.get_raws_sig_data(gacc_region, number_of_years_for_averages, fuel_model, start_date)
        FEMS.get_nfdrs_forecast_data(gacc_region, fuel_model)
    else:
        pass
        
    get_psa_percentiles(gacc_region)
    station_stats(gacc_region)
    get_stats(gacc_region)
    get_psa_climatology(gacc_region)
    sort_data_by_psa(gacc_region)
    station_forecast(gacc_region)
    sort_forecasts_by_psa(gacc_region)

    data_dir = f"FEMS Data/{gacc_region}/PSA Data"
    percentiles_dir = f"FEMS Data/{gacc_region}/PSA Percentiles"
    climo_avg_dir = f"FEMS Data/{gacc_region}/PSA Climo/AVG"
    climo_max_dir = f"FEMS Data/{gacc_region}/PSA Climo/MAX"
    forecast_dir = f"FEMS Data/{gacc_region}/PSA Forecast"

    percentiles = pd.read_csv(f"FEMS Data/{gacc_region}/PSA Percentiles/PSA_Percentiles.csv")

    leap = isleap(utc_time.year)
    if start_date == None:
        if leap == False:
            days = number_of_years_for_averages * 365
        else:
            days = number_of_years_for_averages * 366
        start_date = utc_time - timedelta(days=days)
        start_year = start_date.year
        xmin = start_date
        xmax = utc_time

    else:
        start_date = start_date
        start_year = f"{start_date[0]}{start_date[1]}{start_date[2]}{start_date[3]}"
        start_month = f"{start_date[5]}{start_date[6]}"
        start_day = f"{start_date[8]}{start_date[9]}"
        xmin = datetime(int(start_year), int(start_month), int(start_day))
        xmax = utc_time
    
    psa = 1

    if os.path.exists(f"{data_dir}/.ipynb_checkpoints"):
        shutil.rmtree(f"{data_dir}/.ipynb_checkpoints")
    else:
        pass

    if os.path.exists(f"{data_dir}/.ipynb_checkpoints"):
        shutil.rmtree(f"{data_dir}/.ipynb_checkpoints")
    else:
        pass

    files = os.listdir(f"{data_dir}")
    psa = 1
    psa_IDs = get_psa_ids(gacc_region)
    
    for i in range(0, len(files)):

        fname = f"{psa_IDs[i]}.png"
        psaID = psa_IDs[i]

        try:
            df_data = pd.read_csv(f"{data_dir}/zone_{psa}.csv") 
            try:
                df_forecast = pd.read_csv(f"{forecast_dir}/zone_{psa}.csv") 
            except Exception as e:
                pass
            df_climo_avg = pd.read_csv(f"{climo_avg_dir}/zone_{psa}.csv") 
            df_climo_max = pd.read_csv(f"{climo_max_dir}/zone_{psa}.csv") 
        except Exception as e:
            pass

        try:
            dates = pd.to_datetime(df_data['dates'])
        except Exception as e:
            pass

        fig = plt.figure(figsize=(12,12))

        ax = fig.add_subplot(1, 1, 1)

        ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
        plt.title(f"ENERGY RELEASE COMPONENTS: {gacc_region} PSA {psaID}", fontsize=12, fontweight='bold', loc='left')
        plt.title(f"Period Of Record: {start_year} - {utc_time.year}", fontsize=10, fontweight='bold', loc='right')
        ax.text(0.01, -0.05, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: USDA/FEMS", transform=ax.transAxes, fontsize=8, fontweight='bold', bbox=props)
        ax.text(0.65, -0.05, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=7, fontweight='bold', bbox=props)
        ax.text(0.405, 0.98, f"Valid Date: {dates.iloc[-1].strftime("%m/%d/%Y")}", transform=ax.transAxes, fontsize=8, color='white', fontweight='bold', bbox=date_box)

        if leap == True:
            jmax = 366
        else:
            jmax = 365
        
        ax.set_xlim(0, jmax)

        ymax = np.nanmax(df_climo_max['erc_max']) + 10
        ax.set_ylim(0, ymax)
        
        ax.hlines(percentiles['ERC_60th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='-', alpha=0.5, zorder=2, label=f"60TH PERCENTILE")
        ax.hlines(percentiles['ERC_80th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='--', alpha=0.5, zorder=2, label=f"80TH PERCENTILE")
        ax.hlines(percentiles['ERC_90th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='-.', alpha=0.5, zorder=2, label=f"90TH PERCENTILE")
        ax.hlines(percentiles['ERC_97th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle=':', alpha=0.5, zorder=2, label=f"97TH PERCENTILE")
        ax.hlines(percentiles['ERC_99th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='-', linewidth=2, alpha=0.5, zorder=2, label=f"99TH PERCENTILE")

        ax.axhspan(0, percentiles['ERC_60th_percentile'].iloc[i], color='lime', alpha=0.2, label=f"0TH-60TH PERCENTILE")
        ax.axhspan(percentiles['ERC_60th_percentile'].iloc[i], percentiles['ERC_80th_percentile'].iloc[i], color='lightgreen', alpha=0.2, label=f"60TH-80TH PERCENTILE")
        ax.axhspan(percentiles['ERC_80th_percentile'].iloc[i], percentiles['ERC_90th_percentile'].iloc[i], color='gold', alpha=0.2, label=f"80TH-90TH PERCENTILE")
        ax.axhspan(percentiles['ERC_90th_percentile'].iloc[i], percentiles['ERC_97th_percentile'].iloc[i], color='orange', alpha=0.2, label=f"90TH-97TH PERCENTILE")
        ax.axhspan(percentiles['ERC_97th_percentile'].iloc[i], percentiles['ERC_99th_percentile'].iloc[i], color='red', alpha=0.2, label=f"97TH-99TH PERCENTILE")
        ax.axhspan(percentiles['ERC_99th_percentile'].iloc[i], ymax, color='darkred', alpha=0.2, label=f"ERC>99TH PERCENTILE")

        ax.plot(df_data['julian_date'], df_data['erc_mean'], color='blue', alpha=1, label=f"OBSERVED")
        ax.plot(df_climo_avg['julian_date'], df_climo_avg['erc_avg'], color='gray', alpha=1, label=f"AVERAGE")
        ax.plot(df_climo_max['julian_date'], df_climo_max['erc_max'], color='red', alpha=1, label=f"MAX")
        try:
           ax.plot([df_data['julian_date'].iloc[-1], df_forecast['julian_date'].iloc[0]], [df_data['erc_mean'].iloc[-1], df_forecast['erc_mean'].iloc[0]], color='green', alpha=1)  
           ax.plot(df_forecast['julian_date'], df_forecast['erc_mean'], color='green', alpha=1, label=f"FORECAST") 
        except Exception as e:
            pass
        
        plt.legend(loc="upper left", fontsize="xx-small")

        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        psa = psa + 1

    print(f"ERC Fuels Charts Saved To {path_print}")

def create_psa_bi_fuels_charts(gacc_region, number_of_years_for_averages=15, fuel_model='Y', start_date=None, data=False):
    
    gacc_region = gacc_region.upper()

    path, path_print = file_functions.get_fuels_charts_paths(gacc_region, 'BI')

    if data == False:
        FEMS.get_raws_sig_data(gacc_region, number_of_years_for_averages, fuel_model, start_date)
        FEMS.get_nfdrs_forecast_data(gacc_region, fuel_model)
    else:
        pass
        
    get_psa_percentiles(gacc_region)
    station_stats(gacc_region)
    get_stats(gacc_region)
    get_psa_climatology(gacc_region)
    sort_data_by_psa(gacc_region)
    station_forecast(gacc_region)
    sort_forecasts_by_psa(gacc_region)

    data_dir = f"FEMS Data/{gacc_region}/PSA Data"
    percentiles_dir = f"FEMS Data/{gacc_region}/PSA Percentiles"
    climo_avg_dir = f"FEMS Data/{gacc_region}/PSA Climo/AVG"
    climo_max_dir = f"FEMS Data/{gacc_region}/PSA Climo/MAX"
    forecast_dir = f"FEMS Data/{gacc_region}/PSA Forecast"

    percentiles = pd.read_csv(f"FEMS Data/{gacc_region}/PSA Percentiles/PSA_Percentiles.csv")

    leap = isleap(utc_time.year)
    if start_date == None:
        if leap == False:
            days = number_of_years_for_averages * 365
        else:
            days = number_of_years_for_averages * 366
        start_date = utc_time - timedelta(days=days)
        start_year = start_date.year
        xmin = start_date
        xmax = utc_time

    else:
        start_date = start_date
        start_year = f"{start_date[0]}{start_date[1]}{start_date[2]}{start_date[3]}"
        start_month = f"{start_date[5]}{start_date[6]}"
        start_day = f"{start_date[8]}{start_date[9]}"
        xmin = datetime(int(start_year), int(start_month), int(start_day))
        xmax = utc_time
    
    psa = 1

    if os.path.exists(f"{data_dir}/.ipynb_checkpoints"):
        shutil.rmtree(f"{data_dir}/.ipynb_checkpoints")
    else:
        pass

    if os.path.exists(f"{data_dir}/.ipynb_checkpoints"):
        shutil.rmtree(f"{data_dir}/.ipynb_checkpoints")
    else:
        pass

    files = os.listdir(f"{data_dir}")
    psa = 1
    psa_IDs = get_psa_ids(gacc_region)
    
    for i in range(0, len(files)):

        fname = f"{psa_IDs[i]}.png"
        psaID = psa_IDs[i]

        try:
            df_data = pd.read_csv(f"{data_dir}/zone_{psa}.csv") 
            try:
                df_forecast = pd.read_csv(f"{forecast_dir}/zone_{psa}.csv") 
            except Exception as e:
                pass
            df_climo_avg = pd.read_csv(f"{climo_avg_dir}/zone_{psa}.csv") 
            df_climo_max = pd.read_csv(f"{climo_max_dir}/zone_{psa}.csv") 
        except Exception as e:
            pass

        try:
            dates = pd.to_datetime(df_data['dates'])
        except Exception as e:
            pass

        fig = plt.figure(figsize=(12,12))

        ax = fig.add_subplot(1, 1, 1)

        ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
        plt.title(f"BURNING INDEX: {gacc_region} PSA {psaID}", fontsize=12, fontweight='bold', loc='left')
        plt.title(f"Period Of Record: {start_year} - {utc_time.year}", fontsize=10, fontweight='bold', loc='right')
        ax.text(0.01, -0.05, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: USDA/FEMS", transform=ax.transAxes, fontsize=8, fontweight='bold', bbox=props)
        ax.text(0.65, -0.05, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=7, fontweight='bold', bbox=props)
        ax.text(0.405, 0.98, f"Valid Date: {dates.iloc[-1].strftime("%m/%d/%Y")}", transform=ax.transAxes, fontsize=8, color='white', fontweight='bold', bbox=date_box)

        if leap == True:
            jmax = 366
        else:
            jmax = 365
        
        ax.set_xlim(0, jmax)

        ymax = np.nanmax(df_climo_max['bi_max']) + 10
        ax.set_ylim(0, ymax)
        
        ax.hlines(percentiles['BI_60th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='-', alpha=0.5, zorder=2, label=f"60TH PERCENTILE")
        ax.hlines(percentiles['BI_80th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='--', alpha=0.5, zorder=2, label=f"80TH PERCENTILE")
        ax.hlines(percentiles['BI_90th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='-.', alpha=0.5, zorder=2, label=f"90TH PERCENTILE")
        ax.hlines(percentiles['BI_97th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle=':', alpha=0.5, zorder=2, label=f"97TH PERCENTILE")
        ax.hlines(percentiles['BI_99th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='-', linewidth=2, alpha=0.5, zorder=2, label=f"99TH PERCENTILE")

        ax.axhspan(0, percentiles['BI_60th_percentile'].iloc[i], color='lime', alpha=0.2, label=f"0TH-60TH PERCENTILE")
        ax.axhspan(percentiles['BI_60th_percentile'].iloc[i], percentiles['BI_80th_percentile'].iloc[i], color='lightgreen', alpha=0.2, label=f"60TH-80TH PERCENTILE")
        ax.axhspan(percentiles['BI_80th_percentile'].iloc[i], percentiles['BI_90th_percentile'].iloc[i], color='gold', alpha=0.2, label=f"80TH-90TH PERCENTILE")
        ax.axhspan(percentiles['BI_90th_percentile'].iloc[i], percentiles['BI_97th_percentile'].iloc[i], color='orange', alpha=0.2, label=f"90TH-97TH PERCENTILE")
        ax.axhspan(percentiles['BI_97th_percentile'].iloc[i], percentiles['BI_99th_percentile'].iloc[i], color='red', alpha=0.2, label=f"97TH-99TH PERCENTILE")
        ax.axhspan(percentiles['BI_99th_percentile'].iloc[i], ymax, color='darkred', alpha=0.2, label=f"BI>99TH PERCENTILE")

        ax.plot(df_data['julian_date'], df_data['bi_mean'], color='blue', alpha=1, label=f"OBSERVED")
        ax.plot(df_climo_avg['julian_date'], df_climo_avg['bi_avg'], color='gray', alpha=1, label=f"AVERAGE")
        ax.plot(df_climo_max['julian_date'], df_climo_max['bi_max'], color='red', alpha=1, label=f"MAX")
        try:
           ax.plot([df_data['julian_date'].iloc[-1], df_forecast['julian_date'].iloc[0]], [df_data['bi_mean'].iloc[-1], df_forecast['bi_mean'].iloc[0]], color='green', alpha=1)  
           ax.plot(df_forecast['julian_date'], df_forecast['bi_mean'], color='green', alpha=1, label=f"FORECAST") 
        except Exception as e:
            pass
        
        plt.legend(loc="upper left", fontsize="xx-small")

        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        psa = psa + 1

    print(f"BI Fuels Charts Saved To {path_print}")

def create_psa_sc_fuels_charts(gacc_region, number_of_years_for_averages=15, fuel_model='Y', start_date=None, data=False):
    
    gacc_region = gacc_region.upper()

    path, path_print = file_functions.get_fuels_charts_paths(gacc_region, 'SC')

    if data == False:
        FEMS.get_raws_sig_data(gacc_region, number_of_years_for_averages, fuel_model, start_date)
        FEMS.get_nfdrs_forecast_data(gacc_region, fuel_model)
    else:
        pass
        
    get_psa_percentiles(gacc_region)
    station_stats(gacc_region)
    get_stats(gacc_region)
    get_psa_climatology(gacc_region)
    sort_data_by_psa(gacc_region)
    station_forecast(gacc_region)
    sort_forecasts_by_psa(gacc_region)

    data_dir = f"FEMS Data/{gacc_region}/PSA Data"
    percentiles_dir = f"FEMS Data/{gacc_region}/PSA Percentiles"
    climo_avg_dir = f"FEMS Data/{gacc_region}/PSA Climo/AVG"
    climo_max_dir = f"FEMS Data/{gacc_region}/PSA Climo/MAX"
    forecast_dir = f"FEMS Data/{gacc_region}/PSA Forecast"

    percentiles = pd.read_csv(f"FEMS Data/{gacc_region}/PSA Percentiles/PSA_Percentiles.csv")

    leap = isleap(utc_time.year)
    if start_date == None:
        if leap == False:
            days = number_of_years_for_averages * 365
        else:
            days = number_of_years_for_averages * 366
        start_date = utc_time - timedelta(days=days)
        start_year = start_date.year
        xmin = start_date
        xmax = utc_time

    else:
        start_date = start_date
        start_year = f"{start_date[0]}{start_date[1]}{start_date[2]}{start_date[3]}"
        start_month = f"{start_date[5]}{start_date[6]}"
        start_day = f"{start_date[8]}{start_date[9]}"
        xmin = datetime(int(start_year), int(start_month), int(start_day))
        xmax = utc_time
    
    psa = 1

    if os.path.exists(f"{data_dir}/.ipynb_checkpoints"):
        shutil.rmtree(f"{data_dir}/.ipynb_checkpoints")
    else:
        pass

    if os.path.exists(f"{data_dir}/.ipynb_checkpoints"):
        shutil.rmtree(f"{data_dir}/.ipynb_checkpoints")
    else:
        pass

    files = os.listdir(f"{data_dir}")
    psa = 1
    psa_IDs = get_psa_ids(gacc_region)
    
    for i in range(0, len(files)):

        fname = f"{psa_IDs[i]}.png"
        psaID = psa_IDs[i]

        try:
            df_data = pd.read_csv(f"{data_dir}/zone_{psa}.csv") 
            try:
                df_forecast = pd.read_csv(f"{forecast_dir}/zone_{psa}.csv") 
            except Exception as e:
                pass
            df_climo_avg = pd.read_csv(f"{climo_avg_dir}/zone_{psa}.csv") 
            df_climo_max = pd.read_csv(f"{climo_max_dir}/zone_{psa}.csv") 
        except Exception as e:
            pass

        try:
            dates = pd.to_datetime(df_data['dates'])
        except Exception as e:
            pass

        fig = plt.figure(figsize=(12,12))

        ax = fig.add_subplot(1, 1, 1)

        ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
        plt.title(f"SPREAD COMPONENT: {gacc_region} PSA {psaID}", fontsize=12, fontweight='bold', loc='left')
        plt.title(f"Period Of Record: {start_year} - {utc_time.year}", fontsize=10, fontweight='bold', loc='right')
        ax.text(0.01, -0.05, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: USDA/FEMS", transform=ax.transAxes, fontsize=8, fontweight='bold', bbox=props)
        ax.text(0.65, -0.05, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=7, fontweight='bold', bbox=props)
        ax.text(0.405, 0.98, f"Valid Date: {dates.iloc[-1].strftime("%m/%d/%Y")}", transform=ax.transAxes, fontsize=8, color='white', fontweight='bold', bbox=date_box)

        if leap == True:
            jmax = 366
        else:
            jmax = 365
        
        ax.set_xlim(0, jmax)

        ymax = np.nanmax(df_climo_max['sc_max']) + 10
        ax.set_ylim(0, ymax)
        
        ax.hlines(percentiles['SC_60th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='-', alpha=0.5, zorder=2, label=f"60TH PERCENTILE")
        ax.hlines(percentiles['SC_80th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='--', alpha=0.5, zorder=2, label=f"80TH PERCENTILE")
        ax.hlines(percentiles['SC_90th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='-.', alpha=0.5, zorder=2, label=f"90TH PERCENTILE")
        ax.hlines(percentiles['SC_97th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle=':', alpha=0.5, zorder=2, label=f"97TH PERCENTILE")
        ax.hlines(percentiles['SC_99th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='-', linewidth=2, alpha=0.5, zorder=2, label=f"99TH PERCENTILE")

        ax.axhspan(0, percentiles['SC_60th_percentile'].iloc[i], color='lime', alpha=0.2, label=f"0TH-60TH PERCENTILE")
        ax.axhspan(percentiles['SC_60th_percentile'].iloc[i], percentiles['SC_80th_percentile'].iloc[i], color='lightgreen', alpha=0.2, label=f"60TH-80TH PERCENTILE")
        ax.axhspan(percentiles['SC_80th_percentile'].iloc[i], percentiles['SC_90th_percentile'].iloc[i], color='gold', alpha=0.2, label=f"80TH-90TH PERCENTILE")
        ax.axhspan(percentiles['SC_90th_percentile'].iloc[i], percentiles['SC_97th_percentile'].iloc[i], color='orange', alpha=0.2, label=f"90TH-97TH PERCENTILE")
        ax.axhspan(percentiles['SC_97th_percentile'].iloc[i], percentiles['SC_99th_percentile'].iloc[i], color='red', alpha=0.2, label=f"97TH-99TH PERCENTILE")
        ax.axhspan(percentiles['SC_99th_percentile'].iloc[i], ymax, color='darkred', alpha=0.2, label=f"SC>99TH PERCENTILE")

        ax.plot(df_data['julian_date'], df_data['sc_mean'], color='blue', alpha=1, label=f"OBSERVED")
        ax.plot(df_climo_avg['julian_date'], df_climo_avg['sc_avg'], color='gray', alpha=1, label=f"AVERAGE")
        ax.plot(df_climo_max['julian_date'], df_climo_max['sc_max'], color='red', alpha=1, label=f"MAX")
        try:
           ax.plot([df_data['julian_date'].iloc[-1], df_forecast['julian_date'].iloc[0]], [df_data['sc_mean'].iloc[-1], df_forecast['sc_mean'].iloc[0]], color='green', alpha=1)  
           ax.plot(df_forecast['julian_date'], df_forecast['sc_mean'], color='green', alpha=1, label=f"FORECAST") 
        except Exception as e:
            pass
        
        plt.legend(loc="upper left", fontsize="xx-small")

        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        psa = psa + 1

    print(f"SC Fuels Charts Saved To {path_print}")

def create_psa_ic_fuels_charts(gacc_region, number_of_years_for_averages=15, fuel_model='Y', start_date=None, data=False):
    
    gacc_region = gacc_region.upper()

    path, path_print = file_functions.get_fuels_charts_paths(gacc_region, 'IC')

    if data == False:
        FEMS.get_raws_sig_data(gacc_region, number_of_years_for_averages, fuel_model, start_date)
        FEMS.get_nfdrs_forecast_data(gacc_region, fuel_model)
    else:
        pass
        
    get_psa_percentiles(gacc_region)
    station_stats(gacc_region)
    get_stats(gacc_region)
    get_psa_climatology(gacc_region)
    sort_data_by_psa(gacc_region)
    station_forecast(gacc_region)
    sort_forecasts_by_psa(gacc_region)

    data_dir = f"FEMS Data/{gacc_region}/PSA Data"
    percentiles_dir = f"FEMS Data/{gacc_region}/PSA Percentiles"
    climo_avg_dir = f"FEMS Data/{gacc_region}/PSA Climo/AVG"
    climo_max_dir = f"FEMS Data/{gacc_region}/PSA Climo/MAX"
    forecast_dir = f"FEMS Data/{gacc_region}/PSA Forecast"

    percentiles = pd.read_csv(f"FEMS Data/{gacc_region}/PSA Percentiles/PSA_Percentiles.csv")

    leap = isleap(utc_time.year)
    if start_date == None:
        if leap == False:
            days = number_of_years_for_averages * 365
        else:
            days = number_of_years_for_averages * 366
        start_date = utc_time - timedelta(days=days)
        start_year = start_date.year
        xmin = start_date
        xmax = utc_time

    else:
        start_date = start_date
        start_year = f"{start_date[0]}{start_date[1]}{start_date[2]}{start_date[3]}"
        start_month = f"{start_date[5]}{start_date[6]}"
        start_day = f"{start_date[8]}{start_date[9]}"
        xmin = datetime(int(start_year), int(start_month), int(start_day))
        xmax = utc_time
    
    psa = 1

    if os.path.exists(f"{data_dir}/.ipynb_checkpoints"):
        shutil.rmtree(f"{data_dir}/.ipynb_checkpoints")
    else:
        pass

    if os.path.exists(f"{data_dir}/.ipynb_checkpoints"):
        shutil.rmtree(f"{data_dir}/.ipynb_checkpoints")
    else:
        pass

    files = os.listdir(f"{data_dir}")
    psa = 1
    psa_IDs = get_psa_ids(gacc_region)
    
    for i in range(0, len(files)):

        fname = f"{psa_IDs[i]}.png"
        psaID = psa_IDs[i]

        try:
            df_data = pd.read_csv(f"{data_dir}/zone_{psa}.csv") 
            try:
                df_forecast = pd.read_csv(f"{forecast_dir}/zone_{psa}.csv") 
            except Exception as e:
                pass
            df_climo_avg = pd.read_csv(f"{climo_avg_dir}/zone_{psa}.csv") 
            df_climo_max = pd.read_csv(f"{climo_max_dir}/zone_{psa}.csv") 
        except Exception as e:
            pass

        try:
            dates = pd.to_datetime(df_data['dates'])
        except Exception as e:
            pass

        fig = plt.figure(figsize=(12,12))

        ax = fig.add_subplot(1, 1, 1)

        ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
        plt.title(f"IGNITION COMPONENT: {gacc_region} PSA {psaID}", fontsize=12, fontweight='bold', loc='left')
        plt.title(f"Period Of Record: {start_year} - {utc_time.year}", fontsize=10, fontweight='bold', loc='right')
        ax.text(0.01, -0.05, "Plot Created With FireWxPy (C) Eric J. Drewitz " +utc_time.strftime('%Y')+" | Data Source: USDA/FEMS", transform=ax.transAxes, fontsize=8, fontweight='bold', bbox=props)
        ax.text(0.65, -0.05, "Image Created: " + local_time.strftime(f'%m/%d/%Y %H:%M {timezone}') + " (" + utc_time.strftime('%H:%M UTC') + ")", transform=ax.transAxes, fontsize=7, fontweight='bold', bbox=props)
        ax.text(0.405, 0.98, f"Valid Date: {dates.iloc[-1].strftime("%m/%d/%Y")}", transform=ax.transAxes, fontsize=8, color='white', fontweight='bold', bbox=date_box)

        if leap == True:
            jmax = 366
        else:
            jmax = 365
        
        ax.set_xlim(0, jmax)

        ymax = np.nanmax(df_climo_max['ic_max']) + 10
        ax.set_ylim(0, ymax)
        
        ax.hlines(percentiles['IC_60th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='-', alpha=0.5, zorder=2, label=f"60TH PERCENTILE")
        ax.hlines(percentiles['IC_80th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='--', alpha=0.5, zorder=2, label=f"80TH PERCENTILE")
        ax.hlines(percentiles['IC_90th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='-.', alpha=0.5, zorder=2, label=f"90TH PERCENTILE")
        ax.hlines(percentiles['IC_97th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle=':', alpha=0.5, zorder=2, label=f"97TH PERCENTILE")
        ax.hlines(percentiles['IC_99th_percentile'].iloc[i], xmin=0, xmax=jmax, color='black', linestyle='-', linewidth=2, alpha=0.5, zorder=2, label=f"99TH PERCENTILE")

        ax.axhspan(0, percentiles['IC_60th_percentile'].iloc[i], color='lime', alpha=0.2, label=f"0TH-60TH PERCENTILE")
        ax.axhspan(percentiles['IC_60th_percentile'].iloc[i], percentiles['IC_80th_percentile'].iloc[i], color='lightgreen', alpha=0.2, label=f"60TH-80TH PERCENTILE")
        ax.axhspan(percentiles['IC_80th_percentile'].iloc[i], percentiles['IC_90th_percentile'].iloc[i], color='gold', alpha=0.2, label=f"80TH-90TH PERCENTILE")
        ax.axhspan(percentiles['IC_90th_percentile'].iloc[i], percentiles['IC_97th_percentile'].iloc[i], color='orange', alpha=0.2, label=f"90TH-97TH PERCENTILE")
        ax.axhspan(percentiles['IC_97th_percentile'].iloc[i], percentiles['IC_99th_percentile'].iloc[i], color='red', alpha=0.2, label=f"97TH-99TH PERCENTILE")
        ax.axhspan(percentiles['IC_99th_percentile'].iloc[i], ymax, color='darkred', alpha=0.2, label=f"IC>99TH PERCENTILE")

        ax.plot(df_data['julian_date'], df_data['ic_mean'], color='blue', alpha=1, label=f"OBSERVED")
        ax.plot(df_climo_avg['julian_date'], df_climo_avg['ic_avg'], color='gray', alpha=1, label=f"AVERAGE")
        ax.plot(df_climo_max['julian_date'], df_climo_max['ic_max'], color='red', alpha=1, label=f"MAX")
        try:
           ax.plot([df_data['julian_date'].iloc[-1], df_forecast['julian_date'].iloc[0]], [df_data['ic_mean'].iloc[-1], df_forecast['ic_mean'].iloc[0]], color='green', alpha=1)  
           ax.plot(df_forecast['julian_date'], df_forecast['ic_mean'], color='green', alpha=1, label=f"FORECAST") 
        except Exception as e:
            pass
        
        plt.legend(loc="upper left", fontsize="xx-small")

        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        psa = psa + 1

    print(f"IC Fuels Charts Saved To {path_print}")
