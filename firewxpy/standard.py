'''
This file hosts standard functions which are used across all plotting functions: 

    1) plot_creation_time()
    2) no_data_graphic()
    3) get_timezone()

 This file was written by Meteorologist Eric J. Drewitz 

            (C) Meteorologist Eric J. Drewitz 
                        USDA/USFS
    
'''

#### IMPORTS ####

import pytz
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import time as t

def get_timezone():

    r'''
    This function returns the current timezone abbreviation from the computer's date/time settings.
    Example: Pacific Standard Time = PST

    '''
    now = datetime.now()
    timezone = now.astimezone().tzinfo
    capital_letters = ""
    for char in str(timezone):
        if char.isupper():
            capital_letters += char
            
    return capital_letters


def plot_creation_time():

    r'''
    This function uses the datetime module to find the time at which the script ran. 

    This can be used in many ways:
    1) Timestamp for graphic in both local time and UTC
    2) When downloading data with functions in the data_access module, this function is called to find 
       the time which is passed into the data downloading functions in order for the latest data to be
       downloaded. 

    There are no variables to pass into this function. 

    Returns: 1) Current Local Time
             2) Current UTC Time
            
    '''

    now = datetime.now()
    UTC = now.astimezone(pytz.utc)
    
    sec = now.second
    mn = now.minute
    hr = now.hour
    dy = now.day
    mon = now.month
    yr = now.year
    
    sec1 = UTC.second
    mn1 = UTC.minute
    hr1 = UTC.hour
    dy1 = UTC.day
    mon1 = UTC.month
    yr1 = UTC.year
    
    Local_Time_Now = datetime(yr, mon, dy, hr, mn, sec)
    UTC_Now = datetime(yr1, mon1, dy1, hr1, mn1, sec1)
    
    return Local_Time_Now, UTC_Now


def idle():

    
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second
    sec = minute * 60
    current = second + sec
    resume = 48 * 60
    idle = resume - current
    resume_time = datetime(year, month, day, hour, 48)
    current_time = datetime(year, month, day, hour, minute)
    mins = idle/60

    print("NDFD grid files update on the NWS FTP server from the 17th through 47th minute of the hour.\nThe program will idle until "+resume_time.strftime('%H:%M Local')+".\nYou have "+str(int(round(mins, 0)))+" minutes until the program automatically resumes and tries re-downloading and plotting the data again.")

    print("Current time: "+current_time.strftime('%H:%M Local'))

    t.sleep(idle)

    print("Resuming!")


def no_data_graphic():

    r'''
    This function creates a default graphic for when there is no data present. 
    On the image, it shows the time at which the image was created and that there is
    no data availiable at this time. 

    There are no variables to pass into this function. 

    Returns: 1) A standard graphic stating there is no data available and the time at which the graphic was created. 

    '''
    
    local_time, utc_time = plot_creation_time()
    
    fig = plt.figure(figsize=(20,10))
    ax = plt.subplot(1, 1, 1)
    plt.axis('off')
    fig.text(0.04, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024 | Image Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontsize=20, fontweight='bold')
    ax.text(0.1, 0.6, 'NO DATA FOR: ' + utc_time.strftime('%m/%d/%Y %HZ'), fontsize=60, fontweight='bold')

    return fig

def no_sounding_graphic(date):

    r'''
    This function creates a default graphic for when there is no sounding data present. 
    On the image, it shows the time at which the image was created and that there is
    no data availiable at this time. 

    There are no variables to pass into this function. 

    Returns: 1) A standard graphic stating there is no data available and the time at which the graphic was created. 

    '''
    date = date
    local_time, utc_time = plot_creation_time()
    props = dict(boxstyle='round', facecolor='bisque', alpha=1)
    
    fig = plt.figure(figsize=(5,2))
    ax = plt.subplot(1, 1, 1)
    plt.axis('off')
    fig.text(0.25, 0.08, 'Plot Created With FireWxPy (C) Eric J. Drewitz 2024\nImage Created: ' + local_time.strftime('%m/%d/%Y %H:%M Local') + ' | ' + utc_time.strftime('%m/%d/%Y %H:%M UTC'), fontsize=10, fontweight='bold', bbox=props)
    ax.text(0.1, 0.6, 'NO DATA FOR: ' + date.strftime('%m/%d/%Y %H:00 UTC'), fontsize=20, fontweight='bold')

    return fig






            
