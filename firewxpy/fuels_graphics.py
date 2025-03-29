import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as md
import os
import pandas as pd
import shutil

from data_access import FEMS
from raws_sigs import get_psa_percentiles, sort_data_by_zone
from standard import plot_creation_time
from datetime import datetime, timedelta, UTC
from utilities import file_functions

local_time, utc_time = plot_creation_time()

mpl.rcParams['font.weight'] = 'bold'
props = dict(boxstyle='round', facecolor='wheat', alpha=1)

mpl.rcParams['xtick.labelsize'] = 9
mpl.rcParams['ytick.labelsize'] = 9

def create_psa_100hr_fuels_charts(gacc_region, number_of_years_for_averages=15, fuel_model='Y', start_date=None, data=False):
    
    gacc_region = gacc_region.upper()

    path, path_print = file_functions.get_fuels_charts_paths(gacc_region, '100hr Dead Fuel')

    if data == False:
        FEMS.get_raws_sig_data(gacc_region, number_of_years_for_averages, fuel_model, start_date)
        FEMS.get_nfdrs_forecast_data(gacc_region, fuel_model)
    else:
        pass
        
    get_psa_percentiles(gacc_region)
    sort_data_by_zone(gacc_region)

    data_dir = f"FEMS Data/{gacc_region}/PSA Data"
    percentiles_dir = f"FEMS Data/{gacc_region}/PSA Percentiles"

    percentiles = pd.read_csv(f"FEMS Data/{gacc_region}/PSA Percentiles/PSA_Percentiles.csv")

    if start_date == None:
        days = number_of_years_for_averages * 365
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

    files = os.listdir(f"{data_dir}")
    psa = 1
    for i in range(0, len(files)):

        fname = f"PSA {psa}.png"

        #try:
        df = pd.read_csv(f"{data_dir}/{files[i]}") 

        dates = pd.to_datetime(df['date'])

        fig = plt.figure(figsize=(12,12))

        ax = fig.add_subplot(1, 1, 1)

        ax.xaxis.set_major_formatter(md.DateFormatter('%m-%d'))
        plt.title(f"{gacc_region} 100-HR Dead Fuel Moisture: Zone {psa}", fontsize=12, fontweight='bold', loc='left')
        plt.title(f"Period Of Record: {start_year} - {utc_time.year}", fontsize=10, fontweight='bold', loc='right')

        #ax.hlines(percentiles['100hr_DFM_3_percentile'].iloc[i], xmin=xmin, xmax=xmax, color='black', linestyle='--', alpha=0.5, zorder=2)
        #ax.hlines(percentiles['100hr_DFM_10_percentile'].iloc[i], xmin=xmin, xmax=xmax, color='black', linestyle='--', alpha=0.5, zorder=2)
        #ax.hlines(percentiles['100hr_DFM_20_percentile'].iloc[i], xmin=xmin, xmax=xmax, color='black', linestyle='--', alpha=0.5, zorder=2)
        #ax.hlines(percentiles['100hr_DFM_40_percentile'].iloc[i], xmin=xmin, xmax=xmax, color='black', linestyle='--', alpha=0.5, zorder=2)

        ax.plot(dates, df['100hr_DFM_mean'], color='blue', alpha=1)
        ax.plot(dates, df['100hr_DFM_max'], color='darkgreen', alpha=0.4)
        ax.plot(dates, df['100hr_DFM_min'], color='darkorange', alpha=0.4)
        ax.fill_between(dates, df['100hr_DFM_mean'], df['100hr_DFM_max'], color='green', alpha=0.25, where=(df['100hr_DFM_max'] > df['100hr_DFM_mean']))
        ax.fill_between(dates, df['100hr_DFM_mean'], df['100hr_DFM_min'], color='orange', alpha=0.25, where=(df['100hr_DFM_min'] < df['100hr_DFM_mean']))

        fig.savefig(f"{path}/{fname}", bbox_inches='tight')
        psa = psa + 1
        #except Exception as e:
         #   pass

    
    print(f"100-HR Fuels Charts Saved To {path_print}")

        
    