"""
This file hosts standard functions which are used across all plotting functions: 

    1) plot_creation_time()
    2) no_data_graphic()
    3) get_timezone()

 (C) Eric J. Drewitz 2024-2026
"""

#### IMPORTS ####
try:
    from datetime import datetime, UTC
except Exception as e:
    from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def get_timezone_abbreviation():

    """
    This function returns the current timezone abbreviation from the computer's date/time settings.
    Example: Pacific Standard Time = PST
    
    Required Arguments: None
    
    Optional Arguments: None
    
    Returns
    -------
    
    Timezone abbreviation
    """
    now = datetime.now()
    timezone = now.astimezone().tzinfo
    capital_letters = ""
    for char in str(timezone):
        if char.isupper():
            capital_letters += char
            
    return capital_letters

    
def plot_creation_time():

    """
    This function returns the local and UTC time.  
    
    Required Arguments: None
    
    Optional Arguments: None
    
    Returns
    -------
    
    1) Local Time
    2) UTC Time    
    """
    local = datetime.now()
    
    try:
        utc = datetime.now(UTC)
    except Exception as e:
        utc = datetime.utcnow()
        
    return local, utc

    









            
