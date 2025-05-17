# Table of Contents
[create_psa_100hr_fuels_charts()](https://github.com/edrewitz/firewxpy/new/main/Documentation#create_psa_100hr_fuels_charts)

[create_psa_1000hr_fuels_charts()](https://github.com/edrewitz/firewxpy/new/main/Documentation#create_psa_1000hr_fuels_charts)

[create_psa_erc_fuels_charts()](https://github.com/edrewitz/firewxpy/new/main/Documentation#create_psa_erc_fuels_charts)

[create_psa_bi_fuels_charts()](https://github.com/edrewitz/firewxpy/new/main/Documentation#create_psa_bi_fuels_charts)

[create_psa_sc_fuels_charts()](https://github.com/edrewitz/firewxpy/new/main/Documentation#create_psa_sc_fuels_charts)

[create_psa_ic_fuels_charts()](https://github.com/edrewitz/firewxpy/new/main/Documentation#create_psa_ic_fuels_charts)

### create_psa_100hr_fuels_charts()

This function plots the 100hr dead fuel moisture for each Predictive Services Area for a specific Geographic Area Coordination Center. 

Required Arguments:

1) gacc_region (String) - The 4-letter GACC abbreviation

Optional Arguments: 

1) number_of_years_for_averages (Integer) - Default = 15. The number of years for the average values to be calculated on. 

3) fuel_model (String) - Default = 'Y'. The fuel model being used. 
   Fuel Models List:

   Y - Timber
   X - Brush
   W - Grass/Shrub
   V - Grass
   Z - Slash 

4) start_date (String) - Default = None. If the user wishes to use a selected start date as the starting point enter the start_date
   as a string in the following format: YYYY-mm-dd

5) data (Boolean) - Default = False. When set to False, the function will download the new data. 

   When set to True the function will use the existing data and not download new data. 

   When making multiple types of plots, I recommend setting every function to have data=True except for the first function called in the script. 

Returns

A graphic showing the 100hr dead fuel moisture for each PSA for a specific GACC saved to: f:Fuels Maps/{gacc_region}/100hr Dead Fuel


### create_psa_1000hr_fuels_charts()

This function plots the 1000hr dead fuel moisture for each Predictive Services Area for a specific Geographic Area Coordination Center. 

Required Arguments:

1) gacc_region (String) - The 4-letter GACC abbreviation

Optional Arguments: 

1) number_of_years_for_averages (Integer) - Default = 15. The number of years for the average values to be calculated on. 

3) fuel_model (String) - Default = 'Y'. The fuel model being used. 
   Fuel Models List:

   Y - Timber
   X - Brush
   W - Grass/Shrub
   V - Grass
   Z - Slash 

4) start_date (String) - Default = None. If the user wishes to use a selected start date as the starting point enter the start_date
   as a string in the following format: YYYY-mm-dd

5) data (Boolean) - Default = False. When set to False, the function will download the new data. 

   When set to True the function will use the existing data and not download new data. 

   When making multiple types of plots, I recommend setting every function to have data=True except for the first function called in the script. 

Returns

A graphic showing the 1000hr dead fuel moisture for each PSA for a specific GACC saved to: f:Fuels Maps/{gacc_region}/1000hr Dead Fuel


### create_psa_erc_fuels_charts()

This function plots the Energy Release Component (ERC) Values for each Predictive Services Area for a specific Geographic Area Coordination Center. 

Required Arguments:

1) gacc_region (String) - The 4-letter GACC abbreviation

Optional Arguments: 

1) number_of_years_for_averages (Integer) - Default = 15. The number of years for the average values to be calculated on. 

3) fuel_model (String) - Default = 'Y'. The fuel model being used. 
   Fuel Models List:

   Y - Timber
   X - Brush
   W - Grass/Shrub
   V - Grass
   Z - Slash 

4) start_date (String) - Default = None. If the user wishes to use a selected start date as the starting point enter the start_date
   as a string in the following format: YYYY-mm-dd

5) data (Boolean) - Default = False. When set to False, the function will download the new data. 

   When set to True the function will use the existing data and not download new data. 

   When making multiple types of plots, I recommend setting every function to have data=True except for the first function called in the script. 

Returns

A graphic showing the ERCs for each PSA for a specific GACC saved to: f:Fuels Maps/{gacc_region}/ERC


### create_psa_bi_fuels_charts()

This function plots the Burning Index (BI) for each Predictive Services Area for a specific Geographic Area Coordination Center. 

Required Arguments:

1) gacc_region (String) - The 4-letter GACC abbreviation

Optional Arguments: 

1) number_of_years_for_averages (Integer) - Default = 15. The number of years for the average values to be calculated on. 

3) fuel_model (String) - Default = 'Y'. The fuel model being used. 
   Fuel Models List:

   Y - Timber
   X - Brush
   W - Grass/Shrub
   V - Grass
   Z - Slash 

4) start_date (String) - Default = None. If the user wishes to use a selected start date as the starting point enter the start_date
   as a string in the following format: YYYY-mm-dd

5) data (Boolean) - Default = False. When set to False, the function will download the new data. 

   When set to True the function will use the existing data and not download new data. 

   When making multiple types of plots, I recommend setting every function to have data=True except for the first function called in the script. 

Returns

A graphic showing the BIs for each PSA for a specific GACC saved to: f:Fuels Maps/{gacc_region}/BI

### create_psa_sc_fuels_charts()

This function plots the Spread Component (SC) for each Predictive Services Area for a specific Geographic Area Coordination Center. 

Required Arguments:

1) gacc_region (String) - The 4-letter GACC abbreviation

Optional Arguments: 

1) number_of_years_for_averages (Integer) - Default = 15. The number of years for the average values to be calculated on. 

3) fuel_model (String) - Default = 'Y'. The fuel model being used. 
   Fuel Models List:

   Y - Timber
   X - Brush
   W - Grass/Shrub
   V - Grass
   Z - Slash 

4) start_date (String) - Default = None. If the user wishes to use a selected start date as the starting point enter the start_date
   as a string in the following format: YYYY-mm-dd

5) data (Boolean) - Default = False. When set to False, the function will download the new data. 

   When set to True the function will use the existing data and not download new data. 

   When making multiple types of plots, I recommend setting every function to have data=True except for the first function called in the script. 

Returns

A graphic showing the SCs for each PSA for a specific GACC saved to: f:Fuels Maps/{gacc_region}/SC

### create_psa_ic_fuels_charts()

This function plots the Ignition Component (IC) for each Predictive Services Area for a specific Geographic Area Coordination Center. 

Required Arguments:

1) gacc_region (String) - The 4-letter GACC abbreviation

Optional Arguments: 

1) number_of_years_for_averages (Integer) - Default = 15. The number of years for the average values to be calculated on. 

3) fuel_model (String) - Default = 'Y'. The fuel model being used. 
   Fuel Models List:

   Y - Timber
   X - Brush
   W - Grass/Shrub
   V - Grass
   Z - Slash 

4) start_date (String) - Default = None. If the user wishes to use a selected start date as the starting point enter the start_date
   as a string in the following format: YYYY-mm-dd

5) data (Boolean) - Default = False. When set to False, the function will download the new data. 

   When set to True the function will use the existing data and not download new data. 

   When making multiple types of plots, I recommend setting every function to have data=True except for the first function called in the script. 

Returns

A graphic showing the ICs for each PSA for a specific GACC saved to: f:Fuels Maps/{gacc_region}/IC
















